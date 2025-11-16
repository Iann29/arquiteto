#!/usr/bin/env python3
"""
Toolbar - Barra de ferramentas do Map
"""

import dearpygui.dearpygui as dpg
from nodes.node_registry import NodeRegistry


class Toolbar:
    """Toolbar da aba Map com botões de ação"""

    def __init__(self, callbacks):
        """
        Args:
            callbacks: Dict com callbacks {'add_node': fn, 'delete_nodes': fn, ...}
        """
        self.callbacks = callbacks

    def render(self):
        """Renderiza a toolbar"""
        with dpg.group(horizontal=True):
            # Botão "Adicionar Node" com popup
            add_node_btn = dpg.add_button(label="Adicionar Node")
            with dpg.popup(add_node_btn, modal=False, mousebutton=dpg.mvMouseButton_Left):
                # Pegar nodes da categoria "nodes"
                node_types = NodeRegistry.get_types_by_category("nodes")
                for node_type in node_types:
                    config = NodeRegistry.get_config(node_type)
                    dpg.add_menu_item(
                        label=config["label"].strip(),
                        callback=lambda s, a, u: self.callbacks["add_node"](u),
                        user_data=node_type,
                    )

            # Botão "Editar" com popup
            editar_btn = dpg.add_button(label="Editar")
            with dpg.popup(editar_btn, modal=False, mousebutton=dpg.mvMouseButton_Left):
                dpg.add_menu_item(
                    label="Deletar Nodes Selecionados",
                    callback=self.callbacks.get("delete_nodes"),
                )
                dpg.add_menu_item(
                    label="Deletar Links Selecionados",
                    callback=self.callbacks.get("delete_links"),
                )
                dpg.add_separator()
                dpg.add_menu_item(
                    label="Limpar Tudo",
                    callback=self.callbacks.get("clear_editor"),
                )

            # Botão "Arquivo" com popup
            arquivo_btn = dpg.add_button(label="Arquivo")
            with dpg.popup(arquivo_btn, modal=False, mousebutton=dpg.mvMouseButton_Left):
                dpg.add_menu_item(
                    label="Salvar",
                    callback=self.callbacks.get("save"),
                )
                dpg.add_menu_item(
                    label="Carregar",
                    callback=self.callbacks.get("load"),
                )

        dpg.add_separator()
