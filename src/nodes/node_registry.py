#!/usr/bin/env python3
"""
Node Registry - Registro centralizado de tipos de nodes
"""

import json
from pathlib import Path
from typing import Optional, Dict, List


class NodeRegistry:
    """Gerencia registro de tipos de nodes disponíveis"""

    _config = None
    _config_path = None

    @classmethod
    def load_config(cls):
        """Carrega configuração de nodes do JSON"""
        if cls._config is not None:
            return

        # Path para node_config.json
        cls._config_path = Path(__file__).parent / "node_config.json"

        if not cls._config_path.exists():
            raise FileNotFoundError(
                f"node_config.json não encontrado em {cls._config_path}"
            )

        with open(cls._config_path, "r", encoding="utf-8") as f:
            cls._config = json.load(f)

        print(f"[NodeRegistry] Configuração carregada: {len(cls._config)} tipos de nodes")

    @classmethod
    def get_config(cls, node_type: str) -> Optional[Dict]:
        """
        Retorna configuração de um tipo de node

        Args:
            node_type: Tipo do node (ex: "zed", "abrir")

        Returns:
            Dict com configuração ou None se não encontrado
        """
        if cls._config is None:
            cls.load_config()

        return cls._config.get(node_type)

    @classmethod
    def get_all_types(cls) -> List[str]:
        """Retorna lista de todos os tipos disponíveis"""
        if cls._config is None:
            cls.load_config()

        return list(cls._config.keys())

    @classmethod
    def get_types_by_category(cls, category: str) -> List[str]:
        """
        Retorna tipos filtrados por categoria

        Args:
            category: "nodes" ou "programs"

        Returns:
            Lista de tipos nessa categoria
        """
        if cls._config is None:
            cls.load_config()

        return [
            node_type
            for node_type, config in cls._config.items()
            if config.get("card_category") == category
        ]

    @classmethod
    def is_valid_type(cls, node_type: str) -> bool:
        """Verifica se um tipo é válido"""
        if cls._config is None:
            cls.load_config()

        return node_type in cls._config
