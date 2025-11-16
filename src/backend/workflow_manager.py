#!/usr/bin/env python3
"""
Workflow Manager - Gerenciamento de salvamento e carregamento de workflows
"""

import json
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime


class WorkflowManager:
    """
    Gerencia salvamento e carregamento de workflows em arquivos JSON

    Workflows são salvos em: data/workflows/{nome}.json
    """

    def __init__(self, workflows_dir: Optional[Path] = None):
        """
        Args:
            workflows_dir: Diretório para salvar workflows.
                          Se None, usa data/workflows/ relativo à raiz do projeto
        """
        if workflows_dir is None:
            # Caminho relativo à raiz do projeto (pai de src/)
            project_root = Path(__file__).parent.parent.parent
            self.workflows_dir = project_root / "data" / "workflows"
        else:
            self.workflows_dir = Path(workflows_dir)

        # Criar diretório se não existir
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        print(f"[WorkflowManager] Diretório de workflows: {self.workflows_dir}")

    def save_workflow(
        self, workflow_data: dict, workflow_name: Optional[str] = None
    ) -> bool:
        """
        Salva um workflow em arquivo JSON

        Args:
            workflow_data: Dicionário com dados do workflow (do WorkflowSerializer)
            workflow_name: Nome do arquivo (sem extensão). Se None, usa nome do workflow_data

        Returns:
            True se sucesso, False se erro
        """
        try:
            # Determinar nome do arquivo
            if workflow_name is None:
                workflow_name = workflow_data.get("name", "workflow")

            # Sanitizar nome (remover caracteres inválidos)
            safe_name = self._sanitize_filename(workflow_name)

            # Caminho do arquivo
            file_path = self.workflows_dir / f"{safe_name}.json"

            # Atualizar timestamp de modificação
            workflow_data["updated_at"] = datetime.now().isoformat()

            # Se arquivo já existe, preservar created_at original
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        old_data = json.load(f)
                        workflow_data["created_at"] = old_data.get(
                            "created_at", workflow_data.get("created_at")
                        )
                except Exception:
                    pass  # Se falhar, usa created_at do novo workflow

            # Salvar JSON
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)

            print(f"[WorkflowManager] Workflow salvo: {file_path}")
            return True

        except Exception as e:
            print(f"[WorkflowManager] ERRO ao salvar workflow: {e}")
            import traceback

            traceback.print_exc()
            return False

    def load_workflow(self, workflow_name: str) -> Optional[dict]:
        """
        Carrega um workflow de arquivo JSON

        Args:
            workflow_name: Nome do workflow (sem extensão .json)

        Returns:
            Dicionário com dados do workflow ou None se erro
        """
        try:
            # Sanitizar nome
            safe_name = self._sanitize_filename(workflow_name)

            # Caminho do arquivo
            file_path = self.workflows_dir / f"{safe_name}.json"

            # Verificar se existe
            if not file_path.exists():
                print(f"[WorkflowManager] Workflow não encontrado: {file_path}")
                return None

            # Carregar JSON
            with open(file_path, "r", encoding="utf-8") as f:
                workflow_data = json.load(f)

            print(f"[WorkflowManager] Workflow carregado: {file_path}")
            return workflow_data

        except Exception as e:
            print(f"[WorkflowManager] ERRO ao carregar workflow: {e}")
            import traceback

            traceback.print_exc()
            return None

    def list_workflows(self) -> List[Dict[str, str]]:
        """
        Lista todos os workflows disponíveis

        Returns:
            Lista de dicionários com informações dos workflows:
            [
                {
                    "name": "nome_do_workflow",
                    "file": "nome_do_workflow.json",
                    "created_at": "2025-11-16T10:30:00",
                    "updated_at": "2025-11-16T11:45:00"
                },
                ...
            ]
        """
        workflows = []

        try:
            # Listar todos arquivos .json no diretório
            json_files = sorted(self.workflows_dir.glob("*.json"))

            for file_path in json_files:
                try:
                    # Carregar metadados do workflow
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    workflows.append(
                        {
                            "name": data.get("name", file_path.stem),
                            "file": file_path.stem,
                            "created_at": data.get("created_at", ""),
                            "updated_at": data.get("updated_at", ""),
                            "node_count": len(data.get("nodes", [])),
                            "link_count": len(data.get("links", [])),
                        }
                    )
                except Exception as e:
                    print(
                        f"[WorkflowManager] ERRO ao ler metadados de {file_path}: {e}"
                    )
                    continue

        except Exception as e:
            print(f"[WorkflowManager] ERRO ao listar workflows: {e}")

        return workflows

    def delete_workflow(self, workflow_name: str) -> bool:
        """
        Deleta um workflow

        Args:
            workflow_name: Nome do workflow (sem extensão)

        Returns:
            True se sucesso, False se erro
        """
        try:
            # Sanitizar nome
            safe_name = self._sanitize_filename(workflow_name)

            # Caminho do arquivo
            file_path = self.workflows_dir / f"{safe_name}.json"

            # Verificar se existe
            if not file_path.exists():
                print(f"[WorkflowManager] Workflow não encontrado: {file_path}")
                return False

            # Deletar arquivo
            file_path.unlink()
            print(f"[WorkflowManager] Workflow deletado: {file_path}")
            return True

        except Exception as e:
            print(f"[WorkflowManager] ERRO ao deletar workflow: {e}")
            return False

    def workflow_exists(self, workflow_name: str) -> bool:
        """
        Verifica se um workflow existe

        Args:
            workflow_name: Nome do workflow (sem extensão)

        Returns:
            True se existe, False caso contrário
        """
        safe_name = self._sanitize_filename(workflow_name)
        file_path = self.workflows_dir / f"{safe_name}.json"
        return file_path.exists()

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitiza nome de arquivo removendo caracteres inválidos

        Args:
            name: Nome original

        Returns:
            Nome sanitizado
        """
        # Remover caracteres inválidos para nomes de arquivo
        invalid_chars = '<>:"/\\|?*'
        sanitized = "".join(c if c not in invalid_chars else "_" for c in name)

        # Remover espaços duplos e espaços no início/fim
        sanitized = " ".join(sanitized.split())

        # Limitar tamanho
        max_length = 100
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized.strip()
