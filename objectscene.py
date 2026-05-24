from __future__ import annotations

import random
from abc import ABC, abstractmethod

import pygame
from pygame import Mask, Surface

from assetsutil import Assets, Loader
from config import Config


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------


class Entity(ABC):
    """Contrato mínimo para todo objeto de cena."""

    @abstractmethod
    def move(self) -> None: ...

    @abstractmethod
    def display(self, screen: Surface) -> None: ...


# ---------------------------------------------------------------------------
# Bird
# ---------------------------------------------------------------------------


class Bird(Entity):
    """Pássaro controlado pelo jogador ou pela rede neural."""

    _CONFIG = Config()

    # Constantes carregadas uma única vez por classe
    MAX_ROTATION:            float = _CONFIG.get("bird.max_rotation")
    VEL_ROTATION:            float = _CONFIG.get("bird.rotation_velocity")
    FRAME_ANIMATION:         int   = _CONFIG.get("bird.animation_speed")
    FALLING_ROTATION_LIMIT:  float = _CONFIG.get("bird.falling_rotation_limit")
    FALLING_ANIMATION_ANGLE: float = _CONFIG.get("bird.falling_animation_angle")
    GRAVITY:                 float = _CONFIG.get("bird.gravity")
    JUMP_FORCE:              float = _CONFIG.get("bird.jump_force")
    MAX_FALL_SPEED:          float = _CONFIG.get("bird.max_fall_speed")
    UPWARD_BOOST:            float = _CONFIG.get("bird.upward_boost")

    SPRITES: list[Surface] = [
        Loader.up_scale2x(Assets.BIRD_IDLE),
        Loader.up_scale2x(Assets.BIRD_FLYING),
        Loader.up_scale2x(Assets.BIRD_RUN),
    ]

    # Sequência de frames da animação (índices em SPRITES)
    _ANIMATION_SEQUENCE = [0, 1, 2, 1, 0]

    def __init__(self, axes_x: int, axes_y: int) -> None:
        self.axes_x              = axes_x
        self.axes_y              = axes_y
        self.angle:      float   = 0.0
        self.velocity:   float   = 0.0
        self.height:     int     = axes_y
        self.time:       int     = 0
        self.frame_time: int     = 0
        self.sprit:      Surface = self.SPRITES[0]

    # ------------------------------------------------------------------
    # Física
    # ------------------------------------------------------------------

    def jump(self) -> None:
        self.velocity = self.JUMP_FORCE
        self.time     = 0
        self.height   = self.axes_y

    def move(self) -> None:
        self.time   += 1
        displacement = self._calc_displacement()
        self.axes_y += displacement
        self._update_rotation(displacement)

    def _calc_displacement(self) -> float:
        displacement = self.GRAVITY * (self.time ** 2) + self.velocity * self.time
        if displacement > self.MAX_FALL_SPEED:
            return 16.0

        if displacement < 0:
            displacement -= self.UPWARD_BOOST
        return displacement

    def _update_rotation(self, displacement: float) -> None:
        rising = displacement < 0 or self.axes_y < (self.height + 50)
        if rising:
            self.angle = max(self.angle, self.MAX_ROTATION)
        elif self.angle > self.FALLING_ROTATION_LIMIT:
            self.angle -= self.VEL_ROTATION

    # ------------------------------------------------------------------
    # Renderização
    # ------------------------------------------------------------------

    def display(self, screen: Surface) -> None:
        self._advance_animation()
        self._blit_rotated(screen)

    def _advance_animation(self) -> None:
        """Avança o frame da animação e escolhe o sprite correto."""
        if self.angle <= self.FALLING_ANIMATION_ANGLE:
            # Pássaro caindo: trava no frame do meio
            self.sprit = self.SPRITES[1]
            self.frame_time = self.FRAME_ANIMATION * 2
            return

        cycle_length = self.FRAME_ANIMATION * len(self._ANIMATION_SEQUENCE)
        frame_index = (self.frame_time // self.FRAME_ANIMATION) % len(
            self._ANIMATION_SEQUENCE
        )
        self.sprit = self.SPRITES[self._ANIMATION_SEQUENCE[frame_index]]
        self.frame_time = (self.frame_time + 1) % cycle_length

    def _blit_rotated(self, screen: Surface) -> None:
        rotated = pygame.transform.rotate(self.sprit, self.angle)
        center  = self.sprit.get_rect(topleft=(self.axes_x, self.axes_y)).center
        rect    = rotated.get_rect(center=center)
        screen.blit(rotated, rect.topleft)

    # ------------------------------------------------------------------
    # Colisão
    # ------------------------------------------------------------------

    def get_mask(self) -> Mask:
        return pygame.mask.from_surface(self.sprit)


# ---------------------------------------------------------------------------
# Pipe
# ---------------------------------------------------------------------------


class Pipe(Entity):
    """Par de canos (topo + base) com lacuna aleatória."""

    _CONFIG = Config()

    GAP:        int = _CONFIG.get("pipe.gap")
    VELOCITY:   int = _CONFIG.get("pipe.velocity")
    MIN_HEIGHT: int = _CONFIG.get("pipe.min_height")
    MAX_HEIGHT: int = _CONFIG.get("pipe.max_height")

    _PIPE_IMG: Surface = Loader.up_scale2x(Assets.PIPE)

    def __init__(self, axes_x: int) -> None:
        self.axes_x = axes_x
        self.passed = False

        self.PIPE_TOP:  Surface = pygame.transform.flip(self._PIPE_IMG, False, True)
        self.PIPE_BASE: Surface = self._PIPE_IMG

        # Calculados em _randomize_height
        self.height:   int = 0
        self.pos_top:  int = 0
        self.pos_base: int = 0
        self._randomize_height()

    # ------------------------------------------------------------------
    # Posicionamento
    # ------------------------------------------------------------------

    def _randomize_height(self) -> None:
        self.height   = random.randrange(self.MIN_HEIGHT, self.MAX_HEIGHT)
        self.pos_top  = self.height - self.PIPE_TOP.get_height()
        self.pos_base = self.height + self.GAP

    # ------------------------------------------------------------------
    # Movimento e renderização
    # ------------------------------------------------------------------

    def move(self) -> None:
        self.axes_x -= self.VELOCITY

    def display(self, screen: Surface) -> None:
        screen.blit(self.PIPE_TOP, (self.axes_x, self.pos_top))
        screen.blit(self.PIPE_BASE, (self.axes_x, self.pos_base))

    # ------------------------------------------------------------------
    # Colisão
    # ------------------------------------------------------------------

    def collision_2d(self, bird: Bird) -> bool:
        bird_mask = bird.get_mask()
        top_mask  = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        offset_top  = self._offset(bird, self.pos_top)
        offset_base = self._offset(bird, self.pos_base)

        return bool(
            bird_mask.overlap(top_mask, offset_top)
            or bird_mask.overlap(base_mask, offset_base)
        )

    def _offset(self, bird: Bird, pipe_y: int) -> tuple[int, int]:
        return (self.axes_x - bird.axes_x, pipe_y - round(bird.axes_y))


# ---------------------------------------------------------------------------
# Ground
# ---------------------------------------------------------------------------


class Ground(Entity):
    """Chão com rolagem infinita usando dois tiles lado a lado."""

    _CONFIG = Config()

    VELOCITY: int = _CONFIG.get("ground.velocity")
    SPRITE: Surface = Loader.up_scale2x(Assets.GROUND)
    WIDTH: int = SPRITE.get_width()

    def __init__(self, axes_y: int) -> None:
        self.axes_y = axes_y
        self._x1: int = 0
        self._x2: int = self.WIDTH

    # ------------------------------------------------------------------
    # Movimento e renderização
    # ------------------------------------------------------------------

    def move(self) -> None:
        self._x1 -= self.VELOCITY
        self._x2 -= self.VELOCITY
        self._x1 = self._wrap(self._x1, self._x2)
        self._x2 = self._wrap(self._x2, self._x1)

    def _wrap(self, x: int, other_x: int) -> int:
        """Reposiciona um tile à direita do outro quando sai da tela."""
        if x + self.WIDTH < 0:
            return other_x + self.WIDTH
        return x

    def display(self, screen: Surface) -> None:
        screen.blit(self.SPRITE, (self._x1, self.axes_y))
        screen.blit(self.SPRITE, (self._x2, self.axes_y))