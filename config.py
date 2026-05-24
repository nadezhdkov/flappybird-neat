from __future__ import annotations

import os
from enum       import Enum
from functools  import reduce
from typing     import Any

import yaml


class ConfigurationProvider(Enum):
    CONFIG = "config.yml"


class Config:
    """Carrega e fornece acesso a configurações via notação de ponto.

    Example:
        >>> cfg = Config()
        >>> cfg.get("bird.jump_force")
        -10.5
    """

    _instance: Config | None = None
    _config: dict | None = None

    # ------------------------------------------------------------------
    # Singleton — evita re-leitura do YAML a cada instanciação
    # ------------------------------------------------------------------

    def __new__(cls) -> Config:
        if cls._instance is None:
            cls._instance         = super().__new__(cls)
            cls._instance._config = cls._instance._load()
        return cls._instance

    # ------------------------------------------------------------------
    # Carregamento
    # ------------------------------------------------------------------

    @staticmethod
    def _load() -> dict:
        path = ConfigurationProvider.CONFIG.value
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file not found: '{path}'")
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict):
            raise ValueError(f"Configuration file '{path}' must contain a YAML mapping.")
        return data

    # ------------------------------------------------------------------
    # Acesso
    # ------------------------------------------------------------------

    def get(self, key: str) -> Any:
        """Retorna o valor correspondente à chave em notação de ponto.

        Args:
            key: Caminho separado por pontos, ex: ``"bird.jump_force"``.

        Raises:
            KeyError: Se qualquer segmento do caminho não existir.
        """
        try:
            return reduce(lambda cfg, part: cfg[part], key.split("."), self._config)
        except (KeyError, TypeError):
            raise KeyError(f"Configuration key not found: '{key}'")