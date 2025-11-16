#!/usr/bin/env python3
"""
Node Editor Tab - Aba "Map" com node editor visual
"""

import dearpygui.dearpygui as dpg
from nodes.node_factory import NodeFactory
from .toolbar import Toolbar
from .sidebar import Sidebar
from constants import (
    MAP_SIDEBAR_WIDTH,
    TEXT_COLOR_DARK,
    TEXT_COLOR_COORDS,
)


class NodeEditorTab:
    """Gerencia a aba Map com node editor"""

    def __init__(self):
        self.toolbar = None
        self.sidebar = None

    def show(self):
        """Mostra/cria a aba Map"""
        # Verificar se já existe
        if dpg.does_item_exist("map_tab"):
            dpg.set_value("main_tab_bar", "map_tab")
            return

        # Criar nova aba Map
        with dpg.tab(label="Map", tag="map_tab", parent="main_tab_bar"):
            # Criar toolbar
            callbacks = {
                "add_node": self._add_node_from_toolbar,
                "delete_nodes": self._delete_selected_nodes,
                "delete_links": self._delete_selected_links,
                "clear_editor": self._clear_editor,
                "save": self._menu_callback,
                "load": self._menu_callback,
            }
            self.toolbar = Toolbar(callbacks)
            self.toolbar.render()

            # Layout: Node Editor + Sidebar
            self._create_layout()

            # Footer com coordenadas
            self._create_footer()

        # Selecionar aba
        dpg.set_value("main_tab_bar", "map_tab")
        print("Aba Map criada com Node Editor")

    def _create_layout(self):
        """Cria layout horizontal (editor + sidebar)"""
        with dpg.table(
            header_row=False,
            borders_innerH=False,
            borders_innerV=False,
            borders_outerH=False,
            borders_outerV=False,
            policy=dpg.mvTable_SizingStretchProp,
            resizable=False,
        ) as layout_table:
            dpg.bind_item_theme(layout_table, "map_layout_table_theme")

            # Coluna esquerda: Node Editor (flexível)
            dpg.add_table_column(width_stretch=True, init_width_or_weight=1.0)

            # Coluna direita: Sidebar (fixa)
            dpg.add_table_column(width_fixed=True, init_width_or_weight=MAP_SIDEBAR_WIDTH)

            with dpg.table_row():
                # Node Editor
                with dpg.table_cell():
                    with dpg.child_window(height=-50, border=False, horizontal_scrollbar=False):
                        with dpg.node_editor(
                            callback=self._link_callback,
                            delink_callback=self._delink_callback,
                            tag="map_node_editor",
                        ):
                            # Node inicial: Projeto Iniciado
                            initial_node = NodeFactory.create_node("projeto_iniciado", pos=(20, 20))
                            initial_node.node_id = "node_projeto_iniciado"  # ID fixo para inicial
                            initial_node.render()

                # Sidebar
                with dpg.table_cell():
                    self.sidebar = Sidebar(self._add_node_from_sidebar)
                    self.sidebar.render()

    def _create_footer(self):
        """Cria footer com informações de coordenadas"""
        dpg.add_spacer(height=10)
        with dpg.group(horizontal=True):
            dpg.add_text("Coordenadas:", color=TEXT_COLOR_DARK)
            dpg.add_text("Selecione um node", tag="map_coords_display", color=TEXT_COLOR_COORDS)

    def update_coordinates(self):
        """Atualiza display de coordenadas (chamado a cada frame)"""
        if not dpg.does_item_exist("map_node_editor") or not dpg.does_item_exist(
            "map_coords_display"
        ):
            return

        selected_nodes = dpg.get_selected_nodes("map_node_editor")

        if not selected_nodes or len(selected_nodes) == 0:
            dpg.set_value("map_coords_display", "Selecione um node")
            return

        # Mostrar coordenadas de cada node selecionado
        coords_text = []
        for node_id in selected_nodes:
            pos = dpg.get_item_pos(node_id)
            label = dpg.get_item_label(node_id)
            coords_text.append(f"{label}: ({int(pos[0])}, {int(pos[1])})")

        dpg.set_value("map_coords_display", " | ".join(coords_text))

    # ========================================================================
    # CALLBACKS
    # ========================================================================

    def _add_node_from_toolbar(self, node_type: str):
        """Adiciona node via toolbar"""
        self._add_node(node_type)

    def _add_node_from_sidebar(self, node_type: str):
        """Adiciona node via card da sidebar"""
        self._add_node(node_type)

    def _add_node(self, node_type: str):
        """
        Adiciona um node ao editor

        Args:
            node_type: Tipo do node (ex: "zed", "abrir")
        """
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe!")
            return

        try:
            node = NodeFactory.create_node(node_type)
            node.render(parent="map_node_editor")
        except Exception as e:
            print(f"Erro ao criar node '{node_type}': {e}")

    def _link_callback(self, sender, app_data):
        """Callback quando usuário conecta nodes"""
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        print(f"Link criado: {app_data[0]} -> {app_data[1]}")

    def _delink_callback(self, sender, app_data):
        """Callback quando usuário desconecta nodes"""
        dpg.delete_item(app_data)
        print(f"Link removido: {app_data}")

    def _delete_selected_nodes(self):
        """Deleta nodes selecionados"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        selected_nodes = dpg.get_selected_nodes("map_node_editor")

        if not selected_nodes:
            print("Nenhum node selecionado!")
            return

        for node_id in selected_nodes:
            dpg.delete_item(node_id)
            print(f"Node deletado: {node_id}")

        print(f"Total de {len(selected_nodes)} node(s) deletado(s)")

    def _delete_selected_links(self):
        """Deleta links selecionados"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        selected_links = dpg.get_selected_links("map_node_editor")

        if not selected_links:
            print("Nenhum link selecionado!")
            return

        for link_id in selected_links:
            dpg.delete_item(link_id)
            print(f"Link deletado: {link_id}")

        print(f"Total de {len(selected_links)} link(s) deletado(s)")

    def _clear_editor(self):
        """Limpa todos os nodes e links"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        dpg.delete_item("map_node_editor", children_only=True)
        print("Editor limpo!")

    def _menu_callback(self, sender):
        """Callback genérico para itens de menu (placeholder)"""
        print(f"Menu clicado: {sender}")
