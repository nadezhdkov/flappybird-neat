from __future__     import annotations

import os
from enum           import Enum
from functools      import lru_cache

import pygame
from pygame.surface import Surface

from config         import Config

_CONFIG = Config()
_ASSETS_DIR = "assets"


class Assets(Enum):
    """Identificadores centralizados dos arquivos de assets do jogo."""

    BIRD_IDLE   = _CONFIG.get("assets.bird_idle")
    BIRD_FLYING = _CONFIG.get("assets.bird_flying")
    BIRD_RUN    = _CONFIG.get("assets.bird_run")
    PIPE        = _CONFIG.get("assets.pipe")
    BACKGROUND  = _CONFIG.get("assets.background")
    GROUND      = _CONFIG.get("assets.ground")


class Loader:
    """Carrega e escala assets de imagem, com cache para evitar I/O repetido."""

    @staticmethod
    @lru_cache(maxsize=None)
    def get(asset: Assets) -> Surface:
        """Carrega a imagem correspondente ao asset (resultado cacheado).

        Args:
            asset: Membro de :class:`Assets` a ser carregado.

        Returns:
            Surface pygame com a imagem original.

        Raises:
            FileNotFoundError: Se o arquivo do asset não existir.
        """
        path = os.path.join(_ASSETS_DIR, asset.value)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset file not found: '{path}'")
        return pygame.image.load(path)

    @staticmethod
    @lru_cache(maxsize=None)
    def up_scale2x(asset: Assets) -> Surface:
        """Carrega e escala o asset em 2x (resultado cacheado).

        Args:
            asset: Membro de :class:`Assets` a ser carregado e escalado.

        Returns:
            Surface pygame com a imagem em escala 2x.
        """
        return pygame.transform.scale2x(Loader.get(asset))