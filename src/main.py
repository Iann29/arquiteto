#!/usr/bin/env python3
"""
Arquiteto - Gerenciador de Projetos
GUI reconstruída do zero com DearPyGUI
"""

import dearpygui.dearpygui as dpg

from constants import AVAILABLE_APPS

# Importar módulos do Arquiteto
from database import Database
from project_manager import ProjectManager
from ram_monitor import RAMMonitor
from workspace_manager import WorkspaceManager
from zen_controller import ZenController


class Arquiteto:
    """Aplicação principal do Arquiteto"""

    def __init__(self):
        # Módulos backend
        self.db = Database()
        self.project_manager = ProjectManager(self.db)
        self.workspace_manager = WorkspaceManager()
        self.ram_monitor = RAMMonitor()
        self.zen_controller = ZenController()

        # Reset inicial
        self.db.deactivate_all_projects()

        # Texturas carregadas
        self.textures_loaded = False

    def menu_callback(self, sender):
        """Callback para itens do menu"""
        print(f"Menu clicado: {sender}")

    def add_projeto_iniciado_node(self):
        """Adiciona um novo node 'Projeto Iniciado' no editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe ainda!")
            return

        # Gerar ID único para o node
        import random

        node_id = f"node_projeto_iniciado_{random.randint(1000, 9999)}"
        input_id = f"project_started_input_{random.randint(1000, 9999)}"

        # Criar node no editor
        with dpg.node(
            label="Projeto Iniciado",
            tag=node_id,
            parent="map_node_editor",
            pos=(100, 100),
        ):
            with dpg.node_attribute(
                label="projectStarted", attribute_type=dpg.mvNode_Attr_Static
            ):
                dpg.add_input_text(
                    label="Nome do Projeto",
                    tag=input_id,
                    hint="Ex: uberti, mecanica, amage...",
                    width=200,
                )

            with dpg.node_attribute(
                label="Output", attribute_type=dpg.mvNode_Attr_Output
            ):
                dpg.add_text("Projeto ->")

        print(f"Node 'Projeto Iniciado' adicionado: {node_id}")

    def add_abrir_node(self):
        """Adiciona um novo node 'Abrir' no editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe ainda!")
            return

        # Gerar ID único para o node
        import random

        node_id = f"node_abrir_{random.randint(1000, 9999)}"

        # Criar tema customizado para node "Abrir" (verde #4AA545)
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
                    # Barra de título hover
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarHovered,
                        (64, 155, 59, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Barra de título selecionado
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarSelected,
                        (84, 175, 79, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Padding mínimo e sem borda para manter dimensões compactas
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
                    # Remove fundo dos elementos internos (FrameBg)
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

        # Criar node no editor
        with dpg.node(
            label="  Abrir  ", tag=node_id, parent="map_node_editor", pos=(400, 100)
        ):
            # Input - recebe contexto (projeto, path, etc)
            with dpg.node_attribute(
                label="Input", attribute_type=dpg.mvNode_Attr_Input
            ):
                # Spacer vertical posiciona o pin na mesma altura da imagem
                dpg.add_spacer(width=1, height=1)

            # Atributo de saída contém diretamente a imagem para alinhar o pin ao centro
            with dpg.node_attribute(
                label="Output", attribute_type=dpg.mvNode_Attr_Output
            ):
                if dpg.does_item_exist("tex_abrir"):
                    # Imagem quadrada e compacta que domina o node
                    dpg.add_image("tex_abrir", width=70, height=70)
                else:
                    dpg.add_text("Abrir")

        # Aplicar tema ao node
        dpg.bind_item_theme(node_id, "theme_abrir")

        print(f"Node 'Abrir' adicionado: {node_id}")

    def add_zed_node(self):
        """Adiciona um novo node 'Zed' no editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe ainda!")
            return

        # Gerar ID único para o node
        import random

        node_id = f"node_zed_{random.randint(1000, 9999)}"

        # Criar tema customizado para node "Zed" (azul)
        if not dpg.does_item_exist("theme_zed"):
            with dpg.theme(tag="theme_zed"):
                with dpg.theme_component(dpg.mvNode):
                    # Fundo do node (azul claro)
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackground,
                        (100, 150, 255, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Fundo quando hover
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackgroundHovered,
                        (120, 170, 255, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Fundo quando selecionado
                    dpg.add_theme_color(
                        dpg.mvNodeCol_NodeBackgroundSelected,
                        (150, 200, 255, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Barra de título (azul escuro)
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBar,
                        (50, 100, 200, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Barra de título hover
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarHovered,
                        (70, 120, 220, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )
                    # Barra de título selecionado
                    dpg.add_theme_color(
                        dpg.mvNodeCol_TitleBarSelected,
                        (90, 140, 240, 255),
                        category=dpg.mvThemeCat_Nodes,
                    )

        # Criar node no editor
        with dpg.node(
            label="  Zed  ", tag=node_id, parent="map_node_editor", pos=(400, 250)
        ):
            # Input - recebe contexto
            with dpg.node_attribute(
                label="Input", attribute_type=dpg.mvNode_Attr_Input
            ):
                dpg.add_spacer(width=5, height=5)

            # Conteúdo central - Imagem do Zed
            with dpg.node_attribute(
                label="Content", attribute_type=dpg.mvNode_Attr_Static
            ):
                if dpg.does_item_exist("tex_zed"):
                    with dpg.group(horizontal=True):
                        dpg.add_spacer(width=10)  # Espaço esquerda
                        dpg.add_image("tex_zed", width=60, height=60)
                        dpg.add_spacer(width=10)  # Espaço direita
                else:
                    dpg.add_text("Zed")

            # Output - passa contexto pra frente
            with dpg.node_attribute(
                label="Output", attribute_type=dpg.mvNode_Attr_Output
            ):
                dpg.add_spacer(width=5, height=5)

        # Aplicar tema ao node
        dpg.bind_item_theme(node_id, "theme_zed")

        print(f"Node 'Zed' adicionado: {node_id}")

    def add_claude_node(self):
        """Adiciona um novo node 'Claude' no editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe ainda!")
            return

        # Gerar ID único para o node
        import random

        node_id = f"node_claude_{random.randint(1000, 9999)}"

        # Criar node no editor (sem tema customizado - usa padrão)
        with dpg.node(
            label="  Claude  ", tag=node_id, parent="map_node_editor", pos=(400, 350)
        ):
            # Input - recebe contexto
            with dpg.node_attribute(
                label="Input", attribute_type=dpg.mvNode_Attr_Input
            ):
                dpg.add_spacer(width=5, height=5)

            # Conteúdo central - Imagem do Claude
            with dpg.node_attribute(
                label="Content", attribute_type=dpg.mvNode_Attr_Static
            ):
                if dpg.does_item_exist("tex_claude"):
                    with dpg.group(horizontal=True):
                        dpg.add_spacer(width=10)  # Espaço esquerda
                        dpg.add_image("tex_claude", width=60, height=60)
                        dpg.add_spacer(width=10)  # Espaço direita
                else:
                    dpg.add_text("Claude")

            # Output - passa contexto pra frente
            with dpg.node_attribute(
                label="Output", attribute_type=dpg.mvNode_Attr_Output
            ):
                dpg.add_spacer(width=5, height=5)

        # Node usa tema padrão (sem customização)

        print(f"Node 'Claude' adicionado: {node_id}")

    def link_callback(self, sender, app_data):
        """Callback quando usuário conecta nodes"""
        # app_data -> (link_id1, link_id2)
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        print(f"Link criado: {app_data[0]} -> {app_data[1]}")

    def delink_callback(self, sender, app_data):
        """Callback quando usuário desconecta nodes"""
        # app_data -> link_id
        dpg.delete_item(app_data)
        print(f"Link removido: {app_data}")

    def delete_selected_nodes(self):
        """Deleta nodes selecionados no editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe!")
            return

        # Pegar nodes selecionados
        selected_nodes = dpg.get_selected_nodes("map_node_editor")

        if not selected_nodes:
            print("Nenhum node selecionado!")
            return

        # Deletar cada node selecionado
        for node_id in selected_nodes:
            dpg.delete_item(node_id)
            print(f"Node deletado: {node_id}")

        print(f"Total de {len(selected_nodes)} node(s) deletado(s)")

    def delete_selected_links(self):
        """Deleta links selecionados no editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe!")
            return

        # Pegar links selecionados
        selected_links = dpg.get_selected_links("map_node_editor")

        if not selected_links:
            print("Nenhum link selecionado!")
            return

        # Deletar cada link selecionado
        for link_id in selected_links:
            dpg.delete_item(link_id)
            print(f"Link deletado: {link_id}")

        print(f"Total de {len(selected_links)} link(s) deletado(s)")

    def clear_editor(self):
        """Limpa todos os nodes e links do editor"""
        if not dpg.does_item_exist("map_node_editor"):
            print("Node Editor não existe!")
            return

        dpg.delete_item("map_node_editor", children_only=True)
        print("Editor limpo!")

    def load_textures(self):
        """Carrega texturas para os cards dos nodes"""
        if self.textures_loaded:
            return

        import os
        from pathlib import Path

        # Caminho base para imagens (relativo ao diretório raiz do projeto)
        project_root = Path(__file__).parent.parent
        base_path = str(project_root / "assets" / "nodes")

        # Criar texture registry se não existir
        if not dpg.does_item_exist("texture_registry"):
            dpg.add_texture_registry(tag="texture_registry")

        # Carregar imagem do Projeto Iniciado
        projeto_iniciado_path = os.path.join(base_path, "projeto_iniciado.png")
        if os.path.exists(projeto_iniciado_path):
            width, height, channels, data = dpg.load_image(projeto_iniciado_path)
            dpg.add_static_texture(
                width=width,
                height=height,
                default_value=data,
                tag="tex_projeto_iniciado",
                parent="texture_registry",
            )
            print(f"Textura carregada: projeto_iniciado.png ({width}x{height})")

        # Carregar imagem do Abrir
        abrir_path = os.path.join(base_path, "abrir.png")
        if os.path.exists(abrir_path):
            width, height, channels, data = dpg.load_image(abrir_path)
            dpg.add_static_texture(
                width=width,
                height=height,
                default_value=data,
                tag="tex_abrir",
                parent="texture_registry",
            )
            print(f"Textura carregada: abrir.png ({width}x{height})")

        # Carregar imagens dos programas
        apps_path = str(project_root / "assets" / "apps")

        # Zed
        zed_path = os.path.join(apps_path, "zed-logo.png")
        if os.path.exists(zed_path):
            width, height, channels, data = dpg.load_image(zed_path)
            dpg.add_static_texture(
                width=width,
                height=height,
                default_value=data,
                tag="tex_zed",
                parent="texture_registry",
            )
            print(f"Textura carregada: zed-logo.png ({width}x{height})")

        # Claude AI
        claude_path = os.path.join(apps_path, "claude-ai-icon.png")
        if os.path.exists(claude_path):
            width, height, channels, data = dpg.load_image(claude_path)
            dpg.add_static_texture(
                width=width,
                height=height,
                default_value=data,
                tag="tex_claude",
                parent="texture_registry",
            )
            print(f"Textura carregada: claude-ai-icon.png ({width}x{height})")

        self.textures_loaded = True

    def create_node_card(
        self, label, color, callback, tag, image_tag=None, card_size=100
    ):
        """Cria um card visual para a paleta de nodes"""

        if image_tag and dpg.does_item_exist(image_tag):
            # Card com imagem usando image_button
            with dpg.group(tag=tag):
                # Usar add_image_button para ter imagem clicável
                dpg.add_image_button(
                    texture_tag=image_tag,
                    callback=callback,
                    width=card_size,
                    height=card_size - 25,
                    tag=f"{tag}_btn",
                )
                # Texto abaixo
                dpg.add_text(label, color=(220, 220, 220))
        else:
            # Card sem imagem (fallback para botão colorido)
            with dpg.group(tag=tag):
                # Criar tema customizado para este card
                with dpg.theme(tag=f"{tag}_theme"):
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

                # Criar o botão como card
                btn = dpg.add_button(
                    label=label,
                    callback=callback,
                    width=card_size,
                    height=card_size,
                    tag=f"{tag}_btn",
                )

                # Aplicar tema ao botão
                dpg.bind_item_theme(btn, f"{tag}_theme")

    def update_node_coordinates(self):
        """Atualiza display de coordenadas dos nodes selecionados"""
        if not dpg.does_item_exist("map_node_editor") or not dpg.does_item_exist(
            "map_coords_display"
        ):
            return

        # Pegar nodes selecionados
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

    def show_map_tab(self):
        """Mostra a aba do Map com Node Editor"""
        # Verificar se a aba já existe
        if dpg.does_item_exist("map_tab"):
            # Se já existe, apenas seleciona
            dpg.set_value("main_tab_bar", "map_tab")
            return

        # Criar nova aba Map dentro do tab_bar
        with dpg.tab(label="Map", tag="map_tab", parent="main_tab_bar"):
            # Menu horizontal usando grupos e botões com popup
            with dpg.group(horizontal=True):
                # Botão "Adicionar Node" com popup
                add_node_btn = dpg.add_button(label="Adicionar Node")
                with dpg.popup(
                    add_node_btn, modal=False, mousebutton=dpg.mvMouseButton_Left
                ):
                    dpg.add_menu_item(
                        label="Projeto Iniciado",
                        callback=self.add_projeto_iniciado_node,
                    )
                    dpg.add_menu_item(label="Abrir", callback=self.add_abrir_node)

                # Botão "Editar" com popup
                editar_btn = dpg.add_button(label="Editar")
                with dpg.popup(
                    editar_btn, modal=False, mousebutton=dpg.mvMouseButton_Left
                ):
                    dpg.add_menu_item(
                        label="Deletar Nodes Selecionados",
                        callback=self.delete_selected_nodes,
                    )
                    dpg.add_menu_item(
                        label="Deletar Links Selecionados",
                        callback=self.delete_selected_links,
                    )
                    dpg.add_separator()
                    dpg.add_menu_item(label="Limpar Tudo", callback=self.clear_editor)

                # Botão "Arquivo" com popup
                arquivo_btn = dpg.add_button(label="Arquivo")
                with dpg.popup(
                    arquivo_btn, modal=False, mousebutton=dpg.mvMouseButton_Left
                ):
                    dpg.add_menu_item(label="Salvar", callback=self.menu_callback)
                    dpg.add_menu_item(label="Carregar", callback=self.menu_callback)

            dpg.add_separator()

            # Garantir tema que remove padding interno da tabela usada no layout
            if not dpg.does_item_exist("map_layout_table_theme"):
                with dpg.theme(tag="map_layout_table_theme"):
                    with dpg.theme_component(dpg.mvTable):
                        dpg.add_theme_style(
                            dpg.mvStyleVar_CellPadding,
                            0,
                            0,
                            category=dpg.mvThemeCat_Core,
                        )

            # Layout horizontal: Node Editor + Painel Lateral usando tabela para evitar overflow
            with dpg.table(
                header_row=False,
                borders_innerH=False,
                borders_innerV=False,
                borders_outerH=False,
                borders_outerV=False,
                policy=dpg.mvTable_SizingStretchProp,
                resizable=False,
                tag="map_layout_table",
            ) as map_layout_table:
                dpg.bind_item_theme(map_layout_table, "map_layout_table_theme")

                dpg.add_table_column(width_stretch=True, init_width_or_weight=1.0)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=300.0)

                with dpg.table_row():
                    # Coluna esquerda - Node Editor ocupa todo espaço restante
                    with dpg.table_cell():
                        with dpg.child_window(
                            height=-50, border=False, horizontal_scrollbar=False
                        ):
                            with dpg.node_editor(
                                callback=self.link_callback,
                                delink_callback=self.delink_callback,
                                tag="map_node_editor",
                            ):
                                # Node: Projeto Iniciado
                                with dpg.node(
                                    label="Projeto Iniciado",
                                    tag="node_projeto_iniciado",
                                    pos=(20, 20),
                                ):
                                    with dpg.node_attribute(
                                        label="projectStarted",
                                        attribute_type=dpg.mvNode_Attr_Static,
                                    ):
                                        dpg.add_input_text(
                                            label="Nome do Projeto",
                                            tag="project_started_input",
                                            hint="Ex: uberti, mecanica, amage...",
                                            width=200,
                                        )

                                    with dpg.node_attribute(
                                        label="Output",
                                        attribute_type=dpg.mvNode_Attr_Output,
                                    ):
                                        dpg.add_text("Projeto ->")

                    # Coluna direita - Painel de Paleta (250px fixo)
                    with dpg.table_cell():
                        if not dpg.does_item_exist("palette_panel_theme"):
                            with dpg.theme(tag="palette_panel_theme"):
                                with dpg.theme_component(dpg.mvChildWindow):
                                    dpg.add_theme_style(
                                        dpg.mvStyleVar_WindowPadding,
                                        12,
                                        12,
                                        category=dpg.mvThemeCat_Core,
                                    )

                        with dpg.child_window(
                            height=300,
                            border=True,
                            tag="palette_panel",
                            horizontal_scrollbar=False,
                        ):
                            dpg.bind_item_theme("palette_panel", "palette_panel_theme")
                            dpg.add_text("Nodes Disponíveis", color=(200, 200, 200))
                            dpg.add_separator()
                            dpg.add_spacer(height=10)

                            # Carregar texturas antes de criar os cards
                            self.load_textures()

                            card_definitions = [
                                dict(
                                    label="Projeto Iniciado",
                                    color=(100, 150, 255),
                                    callback=self.add_projeto_iniciado_node,
                                    tag="card_projeto_iniciado",
                                    image_tag="tex_projeto_iniciado",
                                ),
                                dict(
                                    label="Abrir",
                                    color=(150, 255, 150),
                                    callback=self.add_abrir_node,
                                    tag="card_abrir",
                                    image_tag="tex_abrir",
                                ),
                            ]

                            if not dpg.does_item_exist("palette_grid_theme"):
                                with dpg.theme(tag="palette_grid_theme"):
                                    with dpg.theme_component(dpg.mvTable):
                                        dpg.add_theme_style(
                                            dpg.mvStyleVar_CellPadding,
                                            8,
                                            8,
                                            category=dpg.mvThemeCat_Core,
                                        )

                            with dpg.table(
                                header_row=False,
                                borders_innerH=False,
                                borders_innerV=False,
                                borders_outerH=False,
                                borders_outerV=False,
                                policy=dpg.mvTable_SizingStretchProp,
                                resizable=False,
                                tag="palette_grid_table",
                            ) as palette_grid_table:
                                dpg.bind_item_theme(
                                    palette_grid_table, "palette_grid_theme"
                                )

                                dpg.add_table_column(
                                    width_stretch=True, init_width_or_weight=1.0
                                )
                                dpg.add_table_column(
                                    width_stretch=True, init_width_or_weight=1.0
                                )

                                for index in range(0, len(card_definitions), 2):
                                    with dpg.table_row():
                                        for offset in range(2):
                                            card_idx = index + offset
                                            with dpg.table_cell():
                                                if card_idx < len(card_definitions):
                                                    card = card_definitions[card_idx]
                                                    self.create_node_card(**card)
                                                else:
                                                    dpg.add_spacer(height=1)

                        # Separador entre Nodes e Programas
                        dpg.add_spacer(height=15)
                        dpg.add_separator()
                        dpg.add_spacer(height=15)

                        # Painel de Programas Disponíveis
                        with dpg.child_window(
                            height=-50,
                            border=True,
                            tag="programs_panel",
                            horizontal_scrollbar=False,
                        ):
                            dpg.bind_item_theme("programs_panel", "palette_panel_theme")
                            dpg.add_text("Programas Disponíveis", color=(200, 200, 200))
                            dpg.add_separator()
                            dpg.add_spacer(height=10)

                            program_cards = [
                                dict(
                                    label="Zed",
                                    color=(70, 130, 255),
                                    callback=self.add_zed_node,
                                    tag="card_zed",
                                    image_tag="tex_zed",
                                    card_size=80,
                                ),
                                dict(
                                    label="Claude",
                                    color=(217, 119, 87),
                                    callback=self.add_claude_node,
                                    tag="card_claude",
                                    image_tag="tex_claude",
                                    card_size=80,
                                ),
                            ]

                            if not dpg.does_item_exist("programs_grid_theme"):
                                with dpg.theme(tag="programs_grid_theme"):
                                    with dpg.theme_component(dpg.mvTable):
                                        dpg.add_theme_style(
                                            dpg.mvStyleVar_CellPadding,
                                            6,
                                            6,
                                            category=dpg.mvThemeCat_Core,
                                        )

                            with dpg.table(
                                header_row=False,
                                borders_innerH=False,
                                borders_innerV=False,
                                borders_outerH=False,
                                borders_outerV=False,
                                policy=dpg.mvTable_SizingStretchProp,
                                resizable=False,
                                tag="programs_grid_table",
                            ) as programs_grid_table:
                                dpg.bind_item_theme(
                                    programs_grid_table, "programs_grid_theme"
                                )

                                dpg.add_table_column(
                                    width_stretch=True, init_width_or_weight=1.0
                                )
                                dpg.add_table_column(
                                    width_stretch=True, init_width_or_weight=1.0
                                )
                                dpg.add_table_column(
                                    width_stretch=True, init_width_or_weight=1.0
                                )

                                for index in range(0, len(program_cards), 3):
                                    with dpg.table_row():
                                        for offset in range(3):
                                            card_idx = index + offset
                                            with dpg.table_cell():
                                                if card_idx < len(program_cards):
                                                    card = program_cards[card_idx]
                                                    self.create_node_card(**card)
                                                else:
                                                    dpg.add_spacer(height=1)

            # Painel de coordenadas no canto inferior esquerdo
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_text("Coordenadas:", color=(150, 150, 150))
                dpg.add_text(
                    "Selecione um node", tag="map_coords_display", color=(100, 200, 255)
                )

        # Selecionar a nova aba
        dpg.set_value("main_tab_bar", "map_tab")
        print("Aba Map criada com Node Editor")

    def handle_delete_key(self):
        """Handler para tecla Delete - deleta nodes e links selecionados"""
        if not dpg.does_item_exist("map_node_editor"):
            return

        # Pegar nodes selecionados
        selected_nodes = dpg.get_selected_nodes("map_node_editor")

        # Pegar links selecionados
        selected_links = dpg.get_selected_links("map_node_editor")

        # Deletar nodes
        if selected_nodes and len(selected_nodes) > 0:
            for node_id in selected_nodes:
                dpg.delete_item(node_id)
                print(f"Node deletado: {node_id}")

            print(
                f"Total de {len(selected_nodes)} node(s) deletado(s) com tecla Delete"
            )

        # Deletar links
        if selected_links and len(selected_links) > 0:
            for link_id in selected_links:
                dpg.delete_item(link_id)
                print(f"Link deletado: {link_id}")

            print(
                f"Total de {len(selected_links)} link(s) deletado(s) com tecla Delete"
            )

    def setup_gui(self):
        """Configura a interface gráfica do zero"""
        # Criar contexto DearPyGUI
        dpg.create_context()

        # Registrar handler global para tecla Delete
        with dpg.handler_registry():
            dpg.add_key_press_handler(
                dpg.mvKey_Delete, callback=lambda: self.handle_delete_key()
            )

        # Criar viewport
        dpg.create_viewport(
            title="Arquiteto - Gerenciador de Projetos",
            width=1200,
            height=800,
            resizable=True,
        )

        # Criar janela principal com Menu Bar
        with dpg.window(
            tag="main_window",
            label="Arquiteto",
            no_scrollbar=True,
            no_scroll_with_mouse=True,
        ):
            # Menu Bar
            with dpg.menu_bar():
                with dpg.menu(label="Inicio"):
                    dpg.add_menu_item(label="Dashboard", callback=self.menu_callback)
                    dpg.add_separator()
                    dpg.add_menu_item(
                        label="Sair", callback=lambda: dpg.stop_dearpygui()
                    )

                # Menu Map para abrir Node Editor
                dpg.add_menu_item(label="Map", callback=self.show_map_tab)

            # Tab Bar para conteúdo principal
            with dpg.tab_bar(tag="main_tab_bar"):
                # Aba Home
                with dpg.tab(label="Home", tag="home_tab"):
                    dpg.add_text("Bem-vindo ao Arquiteto!")
                    dpg.add_text("Use o menu 'Map' para abrir o Node Editor.")

                # Aba Projetos (vazia - protótipo)
                with dpg.tab(label="Projetos", tag="projetos_tab"):
                    pass

                # Aba Workspaces (vazia - protótipo)
                with dpg.tab(label="Workspaces", tag="workspaces_tab"):
                    pass

                # Aba Status (vazia - protótipo)
                with dpg.tab(label="Status", tag="status_tab"):
                    pass

        # Setup DearPyGUI
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

    def run(self):
        """Loop principal da aplicação"""
        self.setup_gui()

        # Loop de renderização
        while dpg.is_dearpygui_running():
            # Atualizar coordenadas dos nodes selecionados
            self.update_node_coordinates()

            dpg.render_dearpygui_frame()

        # Cleanup
        dpg.destroy_context()


if __name__ == "__main__":
    app = Arquiteto()
    app.run()
