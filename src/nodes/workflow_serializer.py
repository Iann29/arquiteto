#!/usr/bin/env python3
"""
Workflow Serializer - Serialização e deserialização de workflows
Converte estado do editor para JSON e vice-versa
"""

import json
from datetime import datetime
from typing import Optional
import dearpygui.dearpygui as dpg
from .node_state_tracker import NodeStateTracker
from .node_factory import NodeFactory
from .node_types import ProjetoIniciadoNode, WorkspaceNode


class WorkflowSerializer:
    """
    Responsável por serializar e deserializar workflows

    Serialização: Editor -> JSON
    Deserialização: JSON -> Editor
    """

    def __init__(self, tracker: Optional[NodeStateTracker] = None):
        """
        Args:
            tracker: Instância do NodeStateTracker a usar (opcional)
                    Se não fornecido, cria/usa a instância singleton
        """
        self.tracker = tracker if tracker else NodeStateTracker()

    def serialize(self, workflow_name: str = "Novo Workflow") -> dict:
        """
        Serializa o estado atual do editor para um dicionário

        Args:
            workflow_name: Nome do workflow

        Returns:
            Dicionário com estrutura do workflow pronto para JSON
        """
        nodes_data = []
        links_data = []

        # Serializar nodes
        all_nodes = self.tracker.get_all_nodes()
        for node_id, node_info in all_nodes.items():
            node_type = node_info["type"]
            node_instance = node_info["instance"]

            # Pegar posição do node no editor
            pos = [0, 0]
            if dpg.does_item_exist(node_id):
                pos_tuple = dpg.get_item_pos(node_id)
                pos = [pos_tuple[0], pos_tuple[1]]

            # Criar estrutura básica do node
            node_data = {
                "id": node_id,
                "type": node_type,
                "pos": pos,
                "data": {},
            }

            # Extrair dados customizados de acordo com o tipo
            if isinstance(node_instance, ProjetoIniciadoNode):
                project_name = node_instance.get_project_name()
                node_data["data"]["project_name"] = project_name

            elif isinstance(node_instance, WorkspaceNode):
                workspace_number = node_instance.get_workspace_number()
                node_data["data"]["workspace_number"] = workspace_number

            nodes_data.append(node_data)

        # Serializar links
        all_links = self.tracker.get_all_links()
        for link in all_links:
            links_data.append(
                {
                    "id": link["id"],
                    "from_attr": link["from_attr"],
                    "to_attr": link["to_attr"],
                }
            )

        # Estrutura final do workflow
        workflow = {
            "version": "1.0",
            "name": workflow_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "nodes": nodes_data,
            "links": links_data,
        }

        print(
            f"[WorkflowSerializer] Workflow serializado: {len(nodes_data)} nodes, {len(links_data)} links"
        )
        return workflow

    def deserialize(
        self, workflow_data: dict, editor_tag: str = "map_node_editor"
    ) -> bool:
        """
        Deserializa um workflow e reconstrói o editor

        Args:
            workflow_data: Dicionário com dados do workflow
            editor_tag: Tag do node editor no DearPyGUI

        Returns:
            True se sucesso, False se erro
        """
        try:
            # Validar estrutura básica
            if not self._validate_workflow(workflow_data):
                print("[WorkflowSerializer] ERRO: Workflow inválido")
                return False

            # Limpar editor atual
            self._clear_editor(editor_tag)

            # Limpar tracker
            self.tracker.clear()

            # Recriar nodes
            nodes_created = {}
            for node_data in workflow_data["nodes"]:
                node_id = node_data["id"]
                node_type = node_data["type"]
                pos = tuple(node_data["pos"])

                # Criar node via factory
                node = NodeFactory.create_node(node_type, pos, node_id=node_id)

                # Renderizar no editor
                node.render(parent=editor_tag)

                # Restaurar dados customizados
                custom_data = node_data.get("data", {})

                if isinstance(node, ProjetoIniciadoNode):
                    if "project_name" in custom_data:
                        # Definir valor do input_text
                        if dpg.does_item_exist(node.input_id):
                            dpg.set_value(node.input_id, custom_data["project_name"])

                elif isinstance(node, WorkspaceNode):
                    if "workspace_number" in custom_data:
                        # Definir valor do combo
                        if dpg.does_item_exist(node.combo_id):
                            dpg.set_value(
                                node.combo_id, str(custom_data["workspace_number"])
                            )

                # Registrar no tracker
                self.tracker.register_node(node.node_id, node_type, node)

                nodes_created[node.node_id] = node

            # Recriar links
            links_created = 0
            for link_data in workflow_data["links"]:
                from_attr = link_data.get("from_attr")
                to_attr = link_data.get("to_attr")

                # Verificar se atributos existem (foram recriados com os nodes)
                if not from_attr or not to_attr:
                    print(
                        f"[WorkflowSerializer] AVISO: Link ignorado (atributos não especificados)"
                    )
                    continue

                if not dpg.does_item_exist(from_attr) or not dpg.does_item_exist(to_attr):
                    print(
                        f"[WorkflowSerializer] AVISO: Link ignorado (atributos não encontrados): {from_attr} -> {to_attr}"
                    )
                    continue

                # Criar link visual no DearPyGUI
                link_id = dpg.add_node_link(from_attr, to_attr, parent=editor_tag)

                # Registrar no tracker
                self.tracker.register_link(link_id, from_attr, to_attr)
                links_created += 1

            # Marcar como salvo
            self.tracker.mark_as_saved()
            self.tracker.set_current_workflow(workflow_data.get("name", "Workflow"))

            print(
                f"[WorkflowSerializer] Workflow carregado: {len(nodes_created)} nodes, {links_created} links"
            )
            return True

        except Exception as e:
            print(f"[WorkflowSerializer] ERRO ao deserializar workflow: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _validate_workflow(self, workflow_data: dict) -> bool:
        """Valida estrutura básica do workflow"""
        required_keys = ["version", "nodes", "links"]
        for key in required_keys:
            if key not in workflow_data:
                print(f"[WorkflowSerializer] Chave '{key}' não encontrada")
                return False
        return True

    def _clear_editor(self, editor_tag: str):
        """Limpa todos os nodes e links do editor"""
        if not dpg.does_item_exist(editor_tag):
            return

        # Pegar todos os children do node editor
        children = dpg.get_item_children(editor_tag, slot=1)  # slot 1 = children

        if children:
            for child_id in children:
                # Deletar apenas se for node ou link (não deletar UI elements internos)
                item_type = dpg.get_item_type(child_id)
                if "node" in item_type.lower() or "link" in item_type.lower():
                    dpg.delete_item(child_id)

        print("[WorkflowSerializer] Editor limpo")

    def _get_output_attribute(self, node_id: str) -> Optional[int]:
        """
        Pega o ID do atributo de output de um node

        Args:
            node_id: ID do node

        Returns:
            ID do atributo de output ou None
        """
        if not dpg.does_item_exist(node_id):
            return None

        # Pegar children do node
        children = dpg.get_item_children(node_id, slot=1)
        if not children:
            return None

        # Procurar por node_attribute com tipo Output
        for child_id in children:
            item_type = dpg.get_item_type(child_id)
            if "mvAppItemType::mvNode_Attribute" in item_type:
                # Verificar se é output
                config = dpg.get_item_configuration(child_id)
                if config.get("attribute_type") == dpg.mvNode_Attr_Output:
                    return child_id

        return None

    def _get_input_attribute(self, node_id: str) -> Optional[int]:
        """
        Pega o ID do atributo de input de um node

        Args:
            node_id: ID do node

        Returns:
            ID do atributo de input ou None
        """
        if not dpg.does_item_exist(node_id):
            return None

        # Pegar children do node
        children = dpg.get_item_children(node_id, slot=1)
        if not children:
            return None

        # Procurar por node_attribute com tipo Input
        for child_id in children:
            item_type = dpg.get_item_type(child_id)
            if "mvAppItemType::mvNode_Attribute" in item_type:
                # Verificar se é input
                config = dpg.get_item_configuration(child_id)
                if config.get("attribute_type") == dpg.mvNode_Attr_Input:
                    return child_id

        return None
