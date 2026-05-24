from __future__     import annotations

from functools      import lru_cache
from typing         import Sequence

import pygame
from pygame.surface import Surface

import neats
from assetsutil     import Assets, Loader
from config         import Config

# ---------------------------------------------------------------------------
# Configuração global (lida uma vez)
# ---------------------------------------------------------------------------

_cfg = Config()

WINDOWS_WIDTH:  int = _cfg.get("window.width")
WINDOWS_HEIGHT: int = _cfg.get("window.height")

_SCORE_COLOR: tuple[int, int, int] = (
    _cfg.get("colors.score_text.red"),
    _cfg.get("colors.score_text.green"),
    _cfg.get("colors.score_text.blue"),
)
_SCORE_LABEL: str = _cfg.get("score.text")
_GEN_LABEL:   str = _cfg.get("assistent.title")

# ---------------------------------------------------------------------------
# Recursos pygame (inicializados uma vez)
# ---------------------------------------------------------------------------

pygame.font.init()

@lru_cache(maxsize=1)
def _font() -> pygame.font.Font:
    return pygame.font.SysFont(_cfg.get("font.family"), _cfg.get("font.size"))

@lru_cache(maxsize=1)
def _background() -> Surface:
    return Loader.up_scale2x(Assets.BACKGROUND)


# ---------------------------------------------------------------------------
# Renderização de HUD
# ---------------------------------------------------------------------------

def _render_score(screen: Surface, points: int) -> None:
    text = _font().render(f"{_SCORE_LABEL}: {points}", True, _SCORE_COLOR)
    screen.blit(text, (WINDOWS_WIDTH - 10 - text.get_width(), 10))


def _render_generation(screen: Surface) -> None:
    text = _font().render(f"{_GEN_LABEL}: {neats.generation}", True, _SCORE_COLOR)
    screen.blit(text, (10, 10))


# ---------------------------------------------------------------------------
# Ponto de entrada público
# ---------------------------------------------------------------------------

def update(
    screen: Surface,
    targets: Sequence,
    pipes: Sequence,
    ground,
    points: int,
) -> None:
    """Redesenha a cena completa e atualiza o display."""
    screen.blit(_background(), (0, 0))

    for target in targets:
        target.display(screen)

    for pipe in pipes:
        pipe.display(screen)

    _render_score(screen, points)

    if neats.ai_is_playing:
        _render_generation(screen)

    ground.display(screen)
    pygame.display.update()