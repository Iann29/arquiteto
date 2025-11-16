#!/usr/bin/env python3
"""
Theme Manager - Gerenciamento centralizado de temas DearPyGUI
"""

import dearpygui.dearpygui as dpg


class ThemeManager:
    """Gerencia todos os temas do Arquiteto"""

    _themes = {}  # Cache de temas criados

    @classmethod
    def setup_all_themes(cls):
        """Cria todos os temas necessários"""
        cls._create_node_themes()
        cls._create_ui_themes()

    @classmethod
    def _create_node_themes(cls):
        """Cria temas para nodes"""

        # Tema: Node Abrir (verde transparente)
        if not dpg.does_item_exist("theme_abrir"):
            with dpg.theme(tag="theme_abrir"):
                with dpg.theme_component(dpg.mvNode):
                    # Fundo transparente para deixar a imagem dominar o node
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackground,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackgroundHovered,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackgroundSelected,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeOutline,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Barra de título (verde escuro)
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBar,
                        (54, 145, 49, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarHovered,
                        (64, 155, 59, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarSelected,
                        (84, 175, 79, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Padding mínimo e sem borda
                    dpg.add_theme_style(
                        dpg.mvNodeStyleVar_NodePadding,
                        1,
                        1,
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_style(
                        dpg.mvNodeStyleVar_NodeBorderThickness,
                        0,
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_style(
                        dpg.mvNodeStyleVar_NodeCornerRounding,
                        6,
                        category=dpg.mvThemeCat_Nodes,
                    )
                with dpg.theme_component(dpg.mvAll):
                    # Remove fundo dos elementos internos
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBg,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Core,
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgHovered,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Core,
                    )
                    dpg.add_theme_color(
                        dpg.mvThemeCol_FrameBgActive,
                        (0, 0, 0, 0),
                        category=dpg.mvThemeCat_Core,
                    )
            cls._themes["abrir"] = "theme_abrir"

        # Tema: Node Zed (azul)
        if not dpg.does_item_exist("theme_zed"):
            with dpg.theme(tag="theme_zed"):
                with dpg.theme_component(dpg.mvNode):
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackground,
                        (100, 150, 255, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackgroundHovered,
                        (120, 170, 255, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackgroundSelected,
                        (150, 200, 255, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBar,
                        (50, 100, 200, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarHovered,
                        (70, 120, 220, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarSelected,
                        (90, 140, 240, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
            cls._themes["zed"] = "theme_zed"

    @classmethod
    def _create_ui_themes(cls):
        """Cria temas para UI (paletas, tabelas, etc)"""

        # Tema: Tabela do layout do Map (sem padding)
        if not dpg.does_item_exist("map_layout_table_theme"):
            with dpg.theme(tag="map_layout_table_theme"):
                with dpg.theme_component(dpg.mvTable):
                    dpg.add_theme_style(
                        dpg.mvStyleVar_CellPadding,
                        0,
                        0,
                        category=dpg.mvThemeCat_Core,
                    )
            cls._themes["map_layout_table"] = "map_layout_table_theme"

        # Tema: Painel de paleta (padding interno)
        if not dpg.does_item_exist("palette_panel_theme"):
            with dpg.theme(tag="palette_panel_theme"):
                with dpg.theme_component(dpg.mvChildWindow):
                    dpg.add_theme_style(
                        dpg.mvStyleVar_WindowPadding,
                        12,
                        12,
                        category=dpg.mvThemeCat_Core,
                    )
            cls._themes["palette_panel"] = "palette_panel_theme"

        # Tema: Grid de paleta (spacing entre cards)
        if not dpg.does_item_exist("palette_grid_theme"):
            with dpg.theme(tag="palette_grid_theme"):
                with dpg.theme_component(dpg.mvTable):
                    dpg.add_theme_style(
                        dpg.mvStyleVar_CellPadding,
                        8,
                        8,
                        category=dpg.mvThemeCat_Core,
                    )
            cls._themes["palette_grid"] = "palette_grid_theme"

        # Tema: Grid de programas (spacing menor)
        if not dpg.does_item_exist("programs_grid_theme"):
            with dpg.theme(tag="programs_grid_theme"):
                with dpg.theme_component(dpg.mvTable):
                    dpg.add_theme_style(
                        dpg.mvStyleVar_CellPadding,
                        6,
                        6,
                        category=dpg.mvThemeCat_Core,
                    )
            cls._themes["programs_grid"] = "programs_grid_theme"

    @classmethod
    def get_theme(cls, theme_name: str):
        """Retorna o tag do tema pelo nome"""
        return cls._themes.get(theme_name)

    @classmethod
    def create_card_theme(cls, tag: str, color: tuple):
        """
        Cria tema customizado para um card (botão)

        Args:
            tag: Tag única do tema
            color: Tupla RGB (r, g, b)
        """
        if dpg.does_item_exist(tag):
            return tag

        with dpg.theme(tag=tag):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(
                    dpg.mvThemeCol_Button, color, category=dpg.mvThemeCat_Core
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered,
                    (
                        min(255, color[0] + 30),
                        min(255, color[1] + 30),
                        min(255, color[2] + 30),
                    ),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive,
                    (
                        min(255, color[0] + 50),
                        min(255, color[1] + 50),
                        min(255, color[2] + 50),
                    ),
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FrameRounding,
                    8,
                    category=dpg.mvThemeCat_Core,
                )
                dpg.add_theme_style(
                    dpg.mvStyleVar_FramePadding,
                    10,
                    10,
                    category=dpg.mvThemeCat_Core,
                )

        cls._themes[tag] = tag
        return tag
