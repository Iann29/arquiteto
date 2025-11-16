#!/usr/bin/env python3
"""
Dialogs - Janelas modais para interação com usuário
"""

import dearpygui.dearpygui as dpg
from typing import Callable, Optional, List, Dict


class WorkflowDialogs:
    """
    Gerencia dialogs para salvar e carregar workflows

    Dialogs modais para:
    - Salvar workflow (input de texto para nome)
    - Carregar workflow (lista de workflows disponíveis)
    """

    @staticmethod
    def show_save_dialog(
        on_save: Callable[[str], None],
        current_name: Optional[str] = None,
        existing_workflows: Optional[List[str]] = None,
    ):
        """
        Mostra dialog para salvar workflow

        Args:
            on_save: Callback(workflow_name) chamado quando usuário confirma
            current_name: Nome atual do workflow (se existir)
            existing_workflows: Lista de nomes de workflows existentes (para validação)
        """
        if existing_workflows is None:
            existing_workflows = []

        # Deletar dialog anterior se existir
        if dpg.does_item_exist("save_workflow_dialog"):
            dpg.delete_item("save_workflow_dialog")

        # Criar window modal
        with dpg.window(
            label="Salvar Workflow",
            tag="save_workflow_dialog",
            modal=True,
            show=True,
            no_resize=True,
            no_move=False,
            width=400,
            height=180,
            pos=[400, 250],
        ):
            dpg.add_text("Digite um nome para o workflow:")
            dpg.add_spacer(height=5)

            # Input de texto
            dpg.add_input_text(
                tag="save_workflow_name_input",
                default_value=current_name or "",
                hint="Ex: Meu Workflow de Frontend",
                width=-1,
                on_enter=True,
                callback=lambda: WorkflowDialogs._on_save_confirm(
                    on_save, existing_workflows
                ),
            )

            dpg.add_spacer(height=5)

            # Mensagem de erro (inicialmente oculta)
            dpg.add_text(
                "",
                tag="save_workflow_error",
                color=(255, 100, 100),
            )

            dpg.add_spacer(height=10)

            # Botões
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Salvar",
                    width=150,
                    callback=lambda: WorkflowDialogs._on_save_confirm(
                        on_save, existing_workflows
                    ),
                )
                dpg.add_button(
                    label="Cancelar",
                    width=150,
                    callback=lambda: dpg.delete_item("save_workflow_dialog"),
                )

            # Focar no input
            dpg.focus_item("save_workflow_name_input")

    @staticmethod
    def _on_save_confirm(
        on_save: Callable[[str], None], existing_workflows: List[str]
    ):
        """Callback interno para validar e confirmar save"""
        name = dpg.get_value("save_workflow_name_input").strip()

        # Validar nome
        if not name:
            dpg.set_value("save_workflow_error", "⚠️ Digite um nome para o workflow!")
            return

        if len(name) < 3:
            dpg.set_value("save_workflow_error", "⚠️ Nome muito curto (mínimo 3 caracteres)")
            return

        # Verificar se já existe (caso seja novo workflow)
        # Comentado: vamos permitir sobrescrever workflows existentes
        # if name in existing_workflows:
        #     dpg.set_value("save_workflow_error", f"⚠️ Workflow '{name}' já existe!")
        #     return

        # Tudo OK - chamar callback
        on_save(name)

        # Fechar dialog
        dpg.delete_item("save_workflow_dialog")

    @staticmethod
    def show_load_dialog(
        workflows: List[Dict[str, str]],
        on_load: Callable[[str], None],
        on_delete: Optional[Callable[[str], None]] = None,
    ):
        """
        Mostra dialog para carregar workflow

        Args:
            workflows: Lista de dicts com workflows disponíveis
                      [{"name": str, "file": str, "created_at": str, ...}]
            on_load: Callback(workflow_file) chamado quando usuário seleciona
            on_delete: Callback(workflow_file) chamado quando usuário deleta (opcional)
        """
        if not workflows:
            WorkflowDialogs._show_no_workflows_dialog()
            return

        # Deletar dialog anterior se existir
        if dpg.does_item_exist("load_workflow_dialog"):
            dpg.delete_item("load_workflow_dialog")

        # Criar window modal
        with dpg.window(
            label="Carregar Workflow",
            tag="load_workflow_dialog",
            modal=True,
            show=True,
            no_resize=True,
            no_move=False,
            width=500,
            height=400,
            pos=[350, 200],
        ):
            dpg.add_text("Selecione um workflow para carregar:")
            dpg.add_spacer(height=10)

            # Criar mapeamento: label -> workflow_file
            label_to_file = {}
            items = []

            # Lista de workflows (um único radio button com todos os items)
            with dpg.child_window(height=250, border=True):
                # Criar lista de labels com metadados
                for workflow in workflows:
                    meta = f"(Nodes: {workflow.get('node_count', 0)}, Links: {workflow.get('link_count', 0)})"

                    # Adicionar timestamp se disponível
                    if workflow.get("updated_at"):
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(workflow["updated_at"])
                            date_str = dt.strftime("%d/%m %H:%M")
                            meta += f" - {date_str}"
                        except Exception:
                            pass

                    label = f"{workflow['name']} {meta}"
                    items.append(label)
                    label_to_file[label] = workflow["file"]  # Mapear label -> file

                # Radio button único com todos os workflows
                dpg.add_radio_button(
                    items=items,
                    tag="workflow_radio_list",
                    callback=lambda s, a: WorkflowDialogs._on_workflow_selected_label(a, label_to_file),
                )

            dpg.add_spacer(height=10)

            # Workflow selecionado (guardado aqui)
            dpg.add_text(
                "",
                tag="load_workflow_selected",
                show=False,
            )

            # Botões
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Carregar",
                    width=150,
                    callback=lambda: WorkflowDialogs._on_load_confirm(on_load),
                )
                dpg.add_button(
                    label="Cancelar",
                    width=150,
                    callback=lambda: dpg.delete_item("load_workflow_dialog"),
                )

                # Botão deletar (se callback fornecido)
                if on_delete:
                    dpg.add_spacer(width=20)
                    dpg.add_button(
                        label="🗑️ Deletar",
                        width=120,
                        callback=lambda: WorkflowDialogs._on_delete_workflow(on_delete),
                    )

    @staticmethod
    def _on_workflow_selected_label(selected_label: str, label_to_file: Dict[str, str]):
        """
        Callback quando workflow é selecionado (por label)

        Args:
            selected_label: Label (string) selecionado no radio button
            label_to_file: Mapeamento {label: workflow_file}
        """
        # Pegar arquivo correspondente ao label
        if selected_label in label_to_file:
            workflow_file = label_to_file[selected_label]

            # Guardar workflow selecionado
            if dpg.does_item_exist("load_workflow_selected"):
                dpg.set_value("load_workflow_selected", workflow_file)

    @staticmethod
    def _on_load_confirm(on_load: Callable[[str], None]):
        """Callback para confirmar load"""
        if not dpg.does_item_exist("load_workflow_selected"):
            return

        workflow_file = dpg.get_value("load_workflow_selected")

        if not workflow_file:
            print("[WorkflowDialogs] Nenhum workflow selecionado!")
            return

        # Chamar callback
        on_load(workflow_file)

        # Fechar dialog
        dpg.delete_item("load_workflow_dialog")

    @staticmethod
    def _on_delete_workflow(on_delete: Callable[[str], None]):
        """Callback para deletar workflow"""
        if not dpg.does_item_exist("load_workflow_selected"):
            return

        workflow_file = dpg.get_value("load_workflow_selected")

        if not workflow_file:
            print("[WorkflowDialogs] Nenhum workflow selecionado para deletar!")
            return

        # Confirmar deleção
        def _confirm_delete():
            on_delete(workflow_file)
            dpg.delete_item("load_workflow_dialog")

        WorkflowDialogs.show_confirm_dialog(
            title="Confirmar Deleção",
            message=f"Tem certeza que deseja deletar o workflow '{workflow_file}'?\n\nEsta ação não pode ser desfeita!",
            on_confirm=_confirm_delete,
        )

    @staticmethod
    def _show_no_workflows_dialog():
        """Mostra dialog quando não há workflows salvos"""
        # Deletar dialog anterior se existir
        if dpg.does_item_exist("no_workflows_dialog"):
            dpg.delete_item("no_workflows_dialog")

        with dpg.window(
            label="Nenhum Workflow Encontrado",
            tag="no_workflows_dialog",
            modal=True,
            show=True,
            no_resize=True,
            no_move=False,
            width=350,
            height=140,
            pos=[450, 300],
        ):
            dpg.add_text("Nenhum workflow salvo encontrado.")
            dpg.add_spacer(height=5)
            dpg.add_text("Crie seu primeiro workflow e salve!", color=(150, 150, 150))
            dpg.add_spacer(height=15)

            dpg.add_button(
                label="OK",
                width=-1,
                callback=lambda: dpg.delete_item("no_workflows_dialog"),
            )

    @staticmethod
    def show_confirm_dialog(
        title: str,
        message: str,
        on_confirm: Callable[[], None],
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        """
        Dialog genérico de confirmação

        Args:
            title: Título do dialog
            message: Mensagem a exibir
            on_confirm: Callback quando usuário confirma
            on_cancel: Callback quando usuário cancela (opcional)
        """
        # Deletar dialog anterior se existir
        if dpg.does_item_exist("confirm_dialog"):
            dpg.delete_item("confirm_dialog")

        with dpg.window(
            label=title,
            tag="confirm_dialog",
            modal=True,
            show=True,
            no_resize=True,
            no_move=False,
            width=400,
            height=180,
            pos=[400, 250],
        ):
            dpg.add_text(message, wrap=380)
            dpg.add_spacer(height=15)

            with dpg.group(horizontal=True):
                def _on_confirm_click():
                    on_confirm()
                    dpg.delete_item("confirm_dialog")

                def _on_cancel_click():
                    if on_cancel:
                        on_cancel()
                    dpg.delete_item("confirm_dialog")

                dpg.add_button(
                    label="Confirmar",
                    width=150,
                    callback=_on_confirm_click,
                )
                dpg.add_button(
                    label="Cancelar",
                    width=150,
                    callback=_on_cancel_click,
                )

    @staticmethod
    def show_info_dialog(title: str, message: str):
        """
        Dialog simples de informação

        Args:
            title: Título do dialog
            message: Mensagem a exibir
        """
        # Deletar dialog anterior se existir
        if dpg.does_item_exist("info_dialog"):
            dpg.delete_item("info_dialog")

        with dpg.window(
            label=title,
            tag="info_dialog",
            modal=True,
            show=True,
            no_resize=True,
            no_move=False,
            width=350,
            height=140,
            pos=[450, 300],
        ):
            dpg.add_text(message, wrap=330)
            dpg.add_spacer(height=15)

            dpg.add_button(
                label="OK",
                width=-1,
                callback=lambda: dpg.delete_item("info_dialog"),
            )
