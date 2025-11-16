#!/usr/bin/env python3
"""
Node Factory - Factory para criação de nodes
"""

import uuid
from typing import Optional
from .base_node import BaseNode
from .node_registry import NodeRegistry
from .node_types import ProjetoIniciadoNode


class NodeFactory:
    """Factory para criar nodes de forma simplificada"""

    @staticmethod
    def create_node(node_type: str, pos: Optional[tuple] = None):
        """
        Cria um node a partir do tipo

        Args:
            node_type: Tipo do node (ex: "zed", "abrir", "projeto_iniciado")
            pos: Posição (x, y) no editor. Se None, usa default do config

        Returns:
            Instância de BaseNode ou subclasse específica

        Raises:
            ValueError: Se tipo não for válido
        """
        # Validar tipo
        if not NodeRegistry.is_valid_type(node_type):
            raise ValueError(f"Tipo de node '{node_type}' não registrado")

        # Pegar configuração
        config = NodeRegistry.get_config(node_type)

        # Gerar ID único
        node_id = f"node_{node_type}_{uuid.uuid4().hex[:8]}"

        # Usar posição padrão se não fornecida
        if pos is None:
            pos = tuple(config.get("default_pos", (0, 0)))

        # Criar node específico se tiver classe customizada
        if node_type == "projeto_iniciado":
            return ProjetoIniciadoNode(node_id, config, pos)

        # Caso padrão: BaseNode
        return BaseNode(node_id, config, pos)

    @staticmethod
    def generate_node_id(node_type: str) -> str:
        """
        Gera um ID único para um node

        Args:
            node_type: Tipo do node

        Returns:
            String com ID único
        """
        return f"node_{node_type}_{uuid.uuid4().hex[:8]}"
