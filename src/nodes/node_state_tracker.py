#!/usr/bin/env python3
"""
Node State Tracker - Rastreamento de estado do editor de nodes
Mantém registro de todos nodes e links criados no editor
"""


class NodeStateTracker:
    """
    Singleton que rastreia estado completo do editor de nodes

    Mantém registro de:
    - Todos os nodes criados (id, tipo, instância)
    - Todos os links criados (conexões entre nodes)
    - Flag de mudanças não salvas
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa apenas uma vez (singleton pattern)"""
        if not NodeStateTracker._initialized:
            self.nodes = {}  # {node_id: {"type": str, "instance": BaseNode}}
            self.links = []  # [{"id": str, "from_attr": str, "to_attr": str}]
            self.has_unsaved_changes = False
            self.current_workflow_name = None
            NodeStateTracker._initialized = True

    # ===== Node Management =====

    def register_node(self, node_id: str, node_type: str, node_instance):
        """
        Registra um novo node no tracker

        Args:
            node_id: ID único do node
            node_type: Tipo do node (ex: "zed", "projeto_iniciado")
            node_instance: Instância de BaseNode ou subclasse
        """
        self.nodes[node_id] = {
            "type": node_type,
            "instance": node_instance,
        }
        self.has_unsaved_changes = True
        print(f"[NodeStateTracker] Node registrado: {node_id} (tipo: {node_type})")

    def remove_node(self, node_id: str):
        """
        Remove um node do tracker

        Args:
            node_id: ID do node a remover
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.has_unsaved_changes = True
            print(f"[NodeStateTracker] Node removido: {node_id}")

            # Remover links associados a este node (checa pelos atributos)
            self.links = [
                link
                for link in self.links
                if not (link["from_attr"].startswith(node_id) or link["to_attr"].startswith(node_id))
            ]

    def get_node(self, node_id: str):
        """Retorna dados de um node específico"""
        return self.nodes.get(node_id)

    def get_all_nodes(self) -> dict:
        """Retorna dicionário com todos os nodes registrados"""
        return self.nodes.copy()

    def get_node_count(self) -> int:
        """Retorna quantidade de nodes registrados"""
        return len(self.nodes)

    # ===== Link Management =====

    def register_link(self, link_id: str, from_attr: str, to_attr: str):
        """
        Registra um novo link no tracker

        Args:
            link_id: ID único do link (gerado pelo DearPyGUI)
            from_attr: ID do atributo de origem (ex: "node_projeto_iniciado_output")
            to_attr: ID do atributo de destino (ex: "node_abrir_input")
        """
        link_data = {
            "id": link_id,
            "from_attr": from_attr,
            "to_attr": to_attr,
        }
        self.links.append(link_data)
        self.has_unsaved_changes = True
        print(f"[NodeStateTracker] Link registrado: {from_attr} -> {to_attr}")

    def remove_link(self, link_id: str):
        """
        Remove um link do tracker

        Args:
            link_id: ID do link a remover
        """
        self.links = [link for link in self.links if link["id"] != link_id]
        self.has_unsaved_changes = True
        print(f"[NodeStateTracker] Link removido: {link_id}")

    def get_all_links(self) -> list:
        """Retorna lista com todos os links registrados"""
        return self.links.copy()

    def get_link_count(self) -> int:
        """Retorna quantidade de links registrados"""
        return len(self.links)

    # ===== State Management =====

    def clear(self):
        """Limpa todos os nodes e links (usado ao carregar workflow)"""
        self.nodes.clear()
        self.links.clear()
        self.has_unsaved_changes = False
        print("[NodeStateTracker] Estado limpo")

    def mark_as_saved(self):
        """Marca o estado atual como salvo"""
        self.has_unsaved_changes = False

    def set_current_workflow(self, name: str):
        """Define o nome do workflow atual"""
        self.current_workflow_name = name

    def get_current_workflow(self) -> str:
        """Retorna nome do workflow atual ou None"""
        return self.current_workflow_name

    # ===== Debug =====

    def print_state(self):
        """Imprime estado completo do tracker (debug)"""
        print("\n===== NODE STATE TRACKER =====")
        print(f"Workflow atual: {self.current_workflow_name or 'Novo workflow'}")
        print(f"Mudanças não salvas: {self.has_unsaved_changes}")
        print(f"\nNodes registrados: {len(self.nodes)}")
        for node_id, data in self.nodes.items():
            print(f"  - {node_id} (tipo: {data['type']})")
        print(f"\nLinks registrados: {len(self.links)}")
        for link in self.links:
            print(f"  - {link['from_attr']} -> {link['to_attr']}")
        print("==============================\n")
