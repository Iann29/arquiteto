#!/usr/bin/env python3
"""
Node Editor Tab - Aba "Map" com node editor visual
"""

import dearpygui.dearpygui as dpg
from nodes.node_factory import NodeFactory
from nodes.node_state_tracker import NodeStateTracker
from nodes.workflow_serializer import WorkflowSerializer
from backend.workflow_manager import WorkflowManager
from .toolbar import Toolbar
from .sidebar import Sidebar
from .dialogs import WorkflowDialogs
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
        self.tracker = NodeStateTracker()  # Tracker de estado dos nodes/links
        self.serializer = WorkflowSerializer(self.tracker)  # Serializer com o mesmo tracker
        self.workflow_manager = WorkflowManager()  # Manager de I/O de workflows

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
                "save": self._on_save_workflow,
                "load": self._on_load_workflow,
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
                            initial_node = NodeFactory.create_node(
                                "projeto_iniciado",
                                pos=(20, 20),
                                node_id="node_projeto_iniciado",
                            )
                            initial_node.render()

                            # Registrar node inicial no tracker
                            self.tracker.register_node(
                                initial_node.node_id,
                                "projeto_iniciado",
                                initial_node
                            )

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

            # Registrar node no tracker
            self.tracker.register_node(node.node_id, node_type, node)
        except Exception as e:
            print(f"Erro ao criar node '{node_type}': {e}")

    def _get_attribute_tag(self, attr_id: int) -> str:
        """
        Converte ID numérico de atributo para tag customizada

        O DearPyGUI sempre retorna IDs numéricos nos callbacks, mas precisamos
        das tags customizadas para salvar no JSON (para persistência).

        Args:
            attr_id: ID numérico do atributo (ex: 116)

        Returns:
            Tag customizada do atributo (ex: "node_projeto_iniciado_output")
        """
        # Pegar o ID numérico do node parent do atributo
        parent_node_id = dpg.get_item_parent(attr_id)  # Retorna ID numérico (ex: 100)

        # Converter ID numérico do parent para TAG usando get_item_alias()
        # Quando criamos o node com tag="node_projeto_iniciado", essa é a alias!
        parent_node_tag = dpg.get_item_alias(parent_node_id)

        # Se não tiver alias (não deveria acontecer), usar o ID numérico como fallback
        if not parent_node_tag:
            parent_node_tag = str(parent_node_id)
            print(f"[AVISO] Node {parent_node_id} não tem alias/tag! Usando ID numérico.")

        # Pegar configuração do atributo para saber se é input/output/static
        config = dpg.get_item_configuration(attr_id)
        attr_type = config.get("attribute_type")

        # Determinar sufixo baseado no tipo
        if attr_type == dpg.mvNode_Attr_Input:
            suffix = "input"
        elif attr_type == dpg.mvNode_Attr_Output:
            suffix = "output"
        else:
            suffix = "static"

        # Reconstruir a tag customizada
        # Formato: "node_{type}_{uuid}_{suffix}"
        # Ex: "node_projeto_iniciado_9221d629_output"
        attribute_tag = f"{parent_node_tag}_{suffix}"

        return attribute_tag

    def _link_callback(self, sender, app_data):
        """Callback quando usuário conecta nodes"""
        # app_data = (from_attribute, to_attribute)
        # IMPORTANTE: DearPyGUI SEMPRE retorna IDs numéricos (ex: 116, 191)
        # NÃO retorna as tags customizadas!
        from_attr_id = app_data[0]  # ID numérico (ex: 116)
        to_attr_id = app_data[1]    # ID numérico (ex: 191)

        # Converter IDs numéricos para tags customizadas
        # Isso é CRUCIAL para salvar no JSON e recarregar depois!
        from_attr_tag = self._get_attribute_tag(from_attr_id)
        to_attr_tag = self._get_attribute_tag(to_attr_id)

        # Criar link visual (usa IDs numéricos - comportamento nativo)
        link_id = dpg.add_node_link(from_attr_id, to_attr_id, parent=sender)

        # Registrar link no tracker (usando TAGS customizadas!)
        self.tracker.register_link(link_id, from_attr_tag, to_attr_tag)

        print(f"Link criado: {from_attr_tag} -> {to_attr_tag}")

    def _delink_callback(self, sender, app_data):
        """Callback quando usuário desconecta nodes"""
        # app_data = link_id
        link_id = app_data

        # Remover do tracker
        self.tracker.remove_link(link_id)

        # Deletar visualmente
        dpg.delete_item(link_id)
        print(f"Link removido: {link_id}")

    def _delete_selected_nodes(self):
        """Deleta nodes selecionados"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        selected_nodes = dpg.get_selected_nodes("map_node_editor")

        if not selected_nodes:
            print("Nenhum node selecionado!")
            return

        for node_id in selected_nodes:
            # IMPORTANTE: dpg.get_selected_nodes() retorna ID numérico
            # Precisamos converter para TAG usando get_item_alias()
            node_tag = dpg.get_item_alias(node_id)

            if not node_tag:
                node_tag = str(node_id)
                print(f"[AVISO] Node {node_id} não tem alias! Usando ID numérico.")

            # Remover do tracker usando TAG (remove links associados automaticamente)
            self.tracker.remove_node(node_tag)

            # Deletar visualmente
            dpg.delete_item(node_id)
            print(f"Node deletado: {node_tag} (ID: {node_id})")

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
            # Remover do tracker
            self.tracker.remove_link(link_id)

            # Deletar visualmente
            dpg.delete_item(link_id)
            print(f"Link deletado: {link_id}")

        print(f"Total de {len(selected_links)} link(s) deletado(s)")

    def _clear_editor(self):
        """Limpa todos os nodes e links"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        # Limpar tracker
        self.tracker.clear()

        # Limpar visualmente
        dpg.delete_item("map_node_editor", children_only=True)
        print("Editor limpo!")

    # ========================================================================
    # WORKFLOW SAVE/LOAD
    # ========================================================================

    def _on_save_workflow(self):
        """Callback para salvar workflow"""
        # Verificar se workflow atual já tem nome
        current_name = self.tracker.get_current_workflow()

        if current_name:
            # Workflow já tem nome - salvar direto (sobrescrever)
            self._save_workflow_to_file(current_name)
        else:
            # Workflow novo - mostrar dialog para pedir nome
            existing_workflows = [w["file"] for w in self.workflow_manager.list_workflows()]

            WorkflowDialogs.show_save_dialog(
                on_save=self._save_workflow_to_file,
                current_name=current_name,
                existing_workflows=existing_workflows,
            )

    def _save_workflow_to_file(self, workflow_name: str):
        """
        Salva workflow em arquivo JSON

        Args:
            workflow_name: Nome do workflow fornecido pelo usuário
        """
        try:
            # Serializar estado atual do editor
            workflow_data = self.serializer.serialize(workflow_name)

            # Salvar em arquivo
            success = self.workflow_manager.save_workflow(workflow_data, workflow_name)

            if success:
                # Atualizar tracker
                self.tracker.set_current_workflow(workflow_name)
                self.tracker.mark_as_saved()

                # Feedback
                WorkflowDialogs.show_info_dialog(
                    title="Sucesso!",
                    message=f"Workflow '{workflow_name}' salvo com sucesso!",
                )
            else:
                WorkflowDialogs.show_info_dialog(
                    title="Erro",
                    message=f"Erro ao salvar workflow '{workflow_name}'.\nVerifique o console para detalhes.",
                )

        except Exception as e:
            print(f"[NodeEditorTab] ERRO ao salvar workflow: {e}")
            import traceback

            traceback.print_exc()

            WorkflowDialogs.show_info_dialog(
                title="Erro",
                message=f"Erro ao salvar workflow:\n{str(e)}",
            )

    def _on_load_workflow(self):
        """Callback para carregar workflow"""
        # Listar workflows disponíveis
        workflows = self.workflow_manager.list_workflows()

        # Mostrar dialog com lista
        WorkflowDialogs.show_load_dialog(
            workflows=workflows,
            on_load=self._load_workflow_from_file,
            on_delete=self._delete_workflow_file,
        )

    def _load_workflow_from_file(self, workflow_file: str):
        """
        Carrega workflow de arquivo JSON

        Args:
            workflow_file: Nome do arquivo (sem extensão)
        """
        try:
            # Carregar workflow do arquivo
            workflow_data = self.workflow_manager.load_workflow(workflow_file)

            if not workflow_data:
                WorkflowDialogs.show_info_dialog(
                    title="Erro",
                    message=f"Erro ao carregar workflow '{workflow_file}'.\nArquivo não encontrado ou inválido.",
                )
                return

            # Deserializar e reconstruir editor
            success = self.serializer.deserialize(workflow_data, "map_node_editor")

            if success:
                # Feedback
                workflow_name = workflow_data.get("name", workflow_file)
                node_count = len(workflow_data.get("nodes", []))
                link_count = len(workflow_data.get("links", []))

                WorkflowDialogs.show_info_dialog(
                    title="Sucesso!",
                    message=f"Workflow '{workflow_name}' carregado com sucesso!\n\nNodes: {node_count} | Links: {link_count}",
                )
            else:
                WorkflowDialogs.show_info_dialog(
                    title="Erro",
                    message=f"Erro ao carregar workflow '{workflow_file}'.\nVerifique o console para detalhes.",
                )

        except Exception as e:
            print(f"[NodeEditorTab] ERRO ao carregar workflow: {e}")
            import traceback

            traceback.print_exc()

            WorkflowDialogs.show_info_dialog(
                title="Erro",
                message=f"Erro ao carregar workflow:\n{str(e)}",
            )

    def _delete_workflow_file(self, workflow_file: str):
        """
        Deleta um workflow

        Args:
            workflow_file: Nome do arquivo (sem extensão)
        """
        try:
            success = self.workflow_manager.delete_workflow(workflow_file)

            if success:
                # Fechar dialog de load (será reaberto automaticamente se necessário)
                if dpg.does_item_exist("load_workflow_dialog"):
                    dpg.delete_item("load_workflow_dialog")

                # Feedback
                WorkflowDialogs.show_info_dialog(
                    title="Deletado",
                    message=f"Workflow '{workflow_file}' deletado com sucesso!",
                )

                # Reabrir dialog de load (atualizado)
                self._on_load_workflow()
            else:
                WorkflowDialogs.show_info_dialog(
                    title="Erro",
                    message=f"Erro ao deletar workflow '{workflow_file}'.",
                )

        except Exception as e:
            print(f"[NodeEditorTab] ERRO ao deletar workflow: {e}")
            WorkflowDialogs.show_info_dialog(
                title="Erro",
                message=f"Erro ao deletar workflow:\n{str(e)}",
            )
