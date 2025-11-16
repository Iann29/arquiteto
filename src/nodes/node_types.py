#!/usr/bin/env python3
"""
Node Types - Implementações específicas de nodes
"""

import dearpygui.dearpygui as dpg
from .base_node import BaseNode


class ProjetoIniciadoNode(BaseNode):
    """
    Node especial "Projeto Iniciado" que tem input de texto

    Este node é o ponto de partida dos workflows
    """

    def __init__(self, node_id: str, config: dict, pos: tuple = (0, 0)):
        super().__init__(node_id, config, pos)
        self.input_id = f"{node_id}_input"

    def _create_content_attribute(self):
        """
        Override: Cria input de texto para nome do projeto
        """
        with dpg.node_attribute(
            label="projectStarted", attribute_type=dpg.mvNode_Attr_Static
        ):
            dpg.add_input_text(
                label="Nome do Projeto",
                tag=self.input_id,
                hint="Ex: uberti, mecanica, amage...",
                width=200,
            )

    def get_project_name(self) -> str:
        """
        Retorna o nome do projeto digitado no input

        Returns:
            String com nome do projeto ou vazio
        """
        if dpg.does_item_exist(self.input_id):
            return dpg.get_value(self.input_id)
        return ""
