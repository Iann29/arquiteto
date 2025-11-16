#!/usr/bin/env python3
"""
Sidebar - Painéis laterais do Map (paleta de nodes e programas)
"""

import dearpygui.dearpygui as dpg
from nodes.node_registry import NodeRegistry
from .theme_manager import ThemeManager
from constants import TEXT_COLOR_MEDIUM


class Sidebar:
    """Sidebar com paletas de nodes e programas"""

    def __init__(self, add_node_callback):
        """
        Args:
            add_node_callback: Função callback(node_type) para adicionar node
        """
        self.add_node_callback = add_node_callback

    def render(self):
        """Renderiza a sidebar completa"""
        # Painel de Nodes
        with dpg.child_window(
            height=300, border=True, tag="palette_panel", horizontal_scrollbar=False
        ):
            dpg.bind_item_theme("palette_panel", "palette_panel_theme")
            dpg.add_text("Nodes Disponíveis", color=TEXT_COLOR_MEDIUM)
            dpg.add_separator()
            dpg.add_spacer(height=10)

            self._render_palette_grid("nodes", columns=2, theme="palette_grid_theme")

        # Separador
        dpg.add_spacer(height=15)
        dpg.add_separator()
        dpg.add_spacer(height=15)

        # Painel de Programas
        with dpg.child_window(
            height=-50, border=True, tag="programs_panel", horizontal_scrollbar=False
        ):
            dpg.bind_item_theme("programs_panel", "palette_panel_theme")
            dpg.add_text("Programas Disponíveis", color=TEXT_COLOR_MEDIUM)
            dpg.add_separator()
            dpg.add_spacer(height=10)

            self._render_palette_grid("programs", columns=3, theme="programs_grid_theme")

    def _render_palette_grid(self, category: str, columns: int, theme: str):
        """
        Renderiza grid de cards

        Args:
            category: "nodes" ou "programs"
            columns: Número de colunas no grid
            theme: Nome do tema a aplicar
        """
        # Pegar nodes dessa categoria
        node_types = NodeRegistry.get_types_by_category(category)

        # Criar grid (tabela)
        with dpg.table(
            header_row=False,
            borders_innerH=False,
            borders_innerV=False,
            borders_outerH=False,
            borders_outerV=False,
            policy=dpg.mvTable_SizingStretchProp,
            resizable=False,
        ) as grid_table:
            dpg.bind_item_theme(grid_table, theme)

            # Adicionar colunas
            for _ in range(columns):
                dpg.add_table_column(width_stretch=True, init_width_or_weight=1.0)

            # Adicionar cards em linhas
            for index in range(0, len(node_types), columns):
                with dpg.table_row():
                    for offset in range(columns):
                        card_idx = index + offset
                        with dpg.table_cell():
                            if card_idx < len(node_types):
                                node_type = node_types[card_idx]
                                self._create_card(node_type)
                            else:
                                dpg.add_spacer(height=1)

    def _create_card(self, node_type: str):
        """
        Cria um card clicável para um tipo de node

        Args:
            node_type: Tipo do node (ex: "zed")
        """
        config = NodeRegistry.get_config(node_type)
        if not config:
            return

        tag = f"card_{node_type}"
        label = config["label"].strip()
        texture_tag = config.get("texture")
        card_size = config.get("card_size", 100)
        color = tuple(config.get("card_color", (150, 150, 150)))

        # Se tem imagem, usar image_button
        if texture_tag and dpg.does_item_exist(texture_tag):
            with dpg.group(tag=tag):
                dpg.add_image_button(
                    texture_tag=texture_tag,
                    callback=lambda: self.add_node_callback(node_type),
                    width=card_size,
                    height=card_size - 25,
                )
                dpg.add_text(label, color=(220, 220, 220))
        else:
            # Fallback: botão colorido
            with dpg.group(tag=tag):
                # Criar tema para o botão
                theme_tag = ThemeManager.create_card_theme(f"{tag}_theme", color)

                btn = dpg.add_button(
                    label=label,
                    callback=lambda: self.add_node_callback(node_type),
                    width=card_size,
                    height=card_size,
                )

                dpg.bind_item_theme(btn, theme_tag)
