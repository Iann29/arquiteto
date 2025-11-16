#!/usr/bin/env python3
"""
Base Node - Classe base para todos os nodes do Arquiteto
"""

import dearpygui.dearpygui as dpg
from ui.theme_manager import ThemeManager


class BaseNode:
    """Classe base para nodes do editor visual"""

    def __init__(self, node_id: str, config: dict, pos: tuple = (0, 0)):
        """
        Args:
            node_id: ID único do node
            config: Configuração do node (do node_config.json)
            pos: Posição (x, y) no editor
        """
        self.node_id = node_id
        self.config = config
        self.pos = pos

    def render(self, parent="map_node_editor"):
        """
        Renderiza o node no editor

        Args:
            parent: Tag do node editor parent
        """
        with dpg.node(
            label=self.config["label"],
            tag=self.node_id,
            parent=parent,
            pos=self.pos,
        ):
            # Input (se configurado)
            if self.config.get("has_input", False):
                self._create_input_attribute()

            # Content (se configurado)
            if self.config.get("has_content", False):
                self._create_content_attribute()

            # Output (se configurado)
            if self.config.get("has_output", False):
                self._create_output_attribute()

        # Aplicar tema se existir
        self._apply_theme()

        print(f"Node '{self.config['label']}' criado: {self.node_id}")

    def _create_input_attribute(self):
        """Cria atributo de entrada (pin de conexão)"""
        input_tag = f"{self.node_id}_input"
        with dpg.node_attribute(
            label="Input",
            attribute_type=dpg.mvNode_Attr_Input,
            tag=input_tag,
        ):
            dpg.add_spacer(width=1, height=1)

    def _create_content_attribute(self):
        """Cria atributo de conteúdo (centro do node)"""
        with dpg.node_attribute(label="Content", attribute_type=dpg.mvNode_Attr_Static):
            self._render_content()

    def _create_output_attribute(self):
        """Cria atributo de saída (pin de conexão)"""
        output_tag = f"{self.node_id}_output"

        # Caso especial: Node "Abrir" tem imagem NO output
        if self.config.get("output_contains_image", False):
            with dpg.node_attribute(
                label="Output",
                attribute_type=dpg.mvNode_Attr_Output,
                tag=output_tag,
            ):
                self._render_content()
        else:
            with dpg.node_attribute(
                label="Output",
                attribute_type=dpg.mvNode_Attr_Output,
                tag=output_tag,
            ):
                dpg.add_spacer(width=1, height=1)

    def _render_content(self):
        """Renderiza o conteúdo visual do node (imagem ou texto)"""
        texture_tag = self.config.get("texture")

        if texture_tag and dpg.does_item_exist(texture_tag):
            # Renderizar imagem
            w, h = self.config.get("image_size", (60, 60))

            # Programas têm spacing horizontal para centralizar
            if self.config.get("card_category") == "programs":
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=10)
                    dpg.add_image(texture_tag, width=w, height=h)
                    dpg.add_spacer(width=10)
            else:
                dpg.add_image(texture_tag, width=w, height=h)
        else:
            # Fallback: texto
            dpg.add_text(self.config["label"])

    def _apply_theme(self):
        """Aplica tema customizado ao node"""
        theme_name = self.config.get("theme")
        if theme_name:
            theme_tag = ThemeManager.get_theme(theme_name)
            if theme_tag:
                dpg.bind_item_theme(self.node_id, theme_tag)
