#!/usr/bin/env python3
"""
App - Classe principal do Arquiteto (refatorada)
"""

import dearpygui.dearpygui as dpg

# Backend modules
from database import Database
from project_manager import ProjectManager
from workspace_manager import WorkspaceManager
from ram_monitor import RAMMonitor
from zen_controller import ZenController

# UI modules
from ui.theme_manager import ThemeManager
from ui.texture_manager import TextureManager
from ui.main_window import MainWindow

# Nodes
from nodes.node_registry import NodeRegistry

# Constants
from constants import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class Arquiteto:
    """
    Aplicação principal do Arquiteto

    Responsabilidades:
    - Orquestrar backend e frontend
    - Gerenciar lifecycle da aplicação
    - Coordenar módulos (sem implementar UI diretamente)
    """

    def __init__(self):
        # ===== Backend =====
        self.db = Database()
        self.project_manager = ProjectManager(self.db)
        self.workspace_manager = WorkspaceManager()
        self.ram_monitor = RAMMonitor()
        self.zen_controller = ZenController()

        # Reset inicial
        self.db.deactivate_all_projects()

        # ===== Frontend =====
        self.main_window = None

    def setup_gui(self):
        """Configura a interface gráfica"""
        # Criar contexto DearPyGUI
        dpg.create_context()

        # Registrar handler global para tecla Delete
        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Delete, callback=self._handle_delete_key)

        # Carregar configuração de nodes
        NodeRegistry.load_config()

        # Criar temas
        ThemeManager.setup_all_themes()

        # Carregar texturas
        TextureManager.load_all_textures()

        # Criar viewport
        dpg.create_viewport(
            title=WINDOW_TITLE,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            resizable=True,
        )

        # Criar janela principal
        self.main_window = MainWindow()
        self.main_window.setup()

        # Setup DearPyGUI
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

    def run(self):
        """Loop principal da aplicação"""
        self.setup_gui()

        # Loop de renderização
        while dpg.is_dearpygui_running():
            # Atualizar janela principal
            if self.main_window:
                self.main_window.update()

            dpg.render_dearpygui_frame()

        # Cleanup
        dpg.destroy_context()

    def _handle_delete_key(self):
        """Handler global para tecla Delete"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        # Deletar nodes selecionados
        selected_nodes = dpg.get_selected_nodes("map_node_editor")
        if selected_nodes:
            for node_id in selected_nodes:
                dpg.delete_item(node_id)
                print(f"Node deletado: {node_id}")
            print(f"Total de {len(selected_nodes)} node(s) deletado(s)")

        # Deletar links selecionados
        selected_links = dpg.get_selected_links("map_node_editor")
        if selected_links:
            for link_id in selected_links:
                dpg.delete_item(link_id)
                print(f"Link deletado: {link_id}")
            print(f"Total de {len(selected_links)} link(s) deletado(s)")
