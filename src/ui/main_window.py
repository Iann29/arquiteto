#!/usr/bin/env python3
"""
Main Window - Janela principal do Arquiteto
"""

import dearpygui.dearpygui as dpg
from .node_editor_tab import NodeEditorTab


class MainWindow:
    """Gerencia a janela principal e suas tabs"""

    def __init__(self):
        self.node_editor_tab = NodeEditorTab()

    def setup(self):
        """Cria a janela principal"""
        with dpg.window(
            tag="main_window",
            label="Arquiteto",
            no_scrollbar=True,
            no_scroll_with_mouse=True,
        ):
            # Menu Bar
            self._create_menu_bar()

            # Tab Bar
            self._create_tabs()

    def _create_menu_bar(self):
        """Cria menu bar"""
        with dpg.menu_bar():
            with dpg.menu(label="Inicio"):
                dpg.add_menu_item(label="Dashboard", callback=self._menu_callback)
                dpg.add_separator()
                dpg.add_menu_item(label="Sair", callback=lambda: dpg.stop_dearpygui())

            # Menu Map
            dpg.add_menu_item(label="Map", callback=lambda: self.node_editor_tab.show())

    def _create_tabs(self):
        """Cria tab bar com tabs iniciais"""
        with dpg.tab_bar(tag="main_tab_bar"):
            # Aba Home
            with dpg.tab(label="Home", tag="home_tab"):
                dpg.add_text("Bem-vindo ao Arquiteto!")
                dpg.add_text("Use o menu 'Map' para abrir o Node Editor.")

            # Aba Projetos (vazia - futuro)
            with dpg.tab(label="Projetos", tag="projetos_tab"):
                pass

            # Aba Workspaces (vazia - futuro)
            with dpg.tab(label="Workspaces", tag="workspaces_tab"):
                pass

            # Aba Status (vazia - futuro)
            with dpg.tab(label="Status", tag="status_tab"):
                pass

    def update(self):
        """Atualiza elementos da janela (chamado a cada frame)"""
        # Atualizar coordenadas do node editor (se existir)
        if dpg.does_item_exist("map_tab"):
            self.node_editor_tab.update_coordinates()

    def _menu_callback(self, sender):
        """Callback genérico para menu"""
        print(f"Menu clicado: {sender}")
