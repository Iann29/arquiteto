#!/usr/bin/env python3
"""
Node Types - Implementações específicas de nodes
"""

import dearpygui.dearpygui as dpg
from .base_node import BaseNode


class WorkspaceNode(BaseNode):
    """
    Node "Workspace" que permite selecionar um workspace de 1 a 9
    """

    def __init__(self, node_id: str, config: dict, pos: tuple = (0, 0)):
        super().__init__(node_id, config, pos)
        self.combo_id = f"{node_id}_combo"

    def _create_content_attribute(self):
        """
        Override: Cria combo para selecionar workspace (1-9)
        """
        with dpg.node_attribute(
            label="workspaceSelector", attribute_type=dpg.mvNode_Attr_Static
        ):
            dpg.add_combo(
                label="Workspace",
                items=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
                default_value="1",
                tag=self.combo_id,
                width=200,
            )

    def get_workspace_number(self) -> int:
        """
        Retorna o número do workspace selecionado

        Returns:
            int: Número do workspace (1-9)
        """
        if dpg.does_item_exist(self.combo_id):
            value = dpg.get_value(self.combo_id)
            return int(value)
        return 1


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
