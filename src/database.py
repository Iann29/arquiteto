#!/usr/bin/env python3
"""
Database - Gerenciamento de projetos com SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any


class Database:
    def __init__(self, db_path: str = "projects.db"):
        # Se path relativo, usar diretório data/
        if not Path(db_path).is_absolute():
            # Path relativo ao diretório raiz do projeto (pai de src/)
            project_root = Path(__file__).parent.parent
            self.db_path = str(project_root / "data" / db_path)
        else:
            self.db_path = db_path
        self.init_database()
        self.migrate_add_hotkeys()  # Migração: adicionar colunas de hotkeys

    def init_database(self):
        """Inicializa o banco de dados e cria tabelas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                folder_path TEXT NOT NULL,
                zen_container TEXT,
                workspace_1_app TEXT,
                workspace_2_app TEXT,
                workspace_3_app TEXT,
                custom_commands TEXT,
                urls TEXT,
                last_opened TIMESTAMP,
                is_active BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def migrate_add_hotkeys(self):
        """Migração: adiciona colunas de hotkeys se não existirem"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Verifica se colunas já existem
            cursor.execute("PRAGMA table_info(projects)")
            columns = [col[1] for col in cursor.fetchall()]

            # Adiciona colunas se não existirem
            for ws_num in [1, 2, 3]:
                col_name = f"workspace_{ws_num}_hotkey"
                if col_name not in columns:
                    cursor.execute(f"ALTER TABLE projects ADD COLUMN {col_name} TEXT DEFAULT ''")
                    print(f"[MIGRAÇÃO] Coluna '{col_name}' adicionada ao banco")

            conn.commit()
        except Exception as e:
            print(f"Erro na migração de hotkeys: {e}")
        finally:
            conn.close()

    def get_connection(self):
        """Retorna uma conexao com o banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_project(self, name: str, folder_path: str, **kwargs) -> Optional[int]:
        """Cria um novo projeto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Preparar dados opcionais
            zen_container = kwargs.get("zen_container", "")
            workspace_1_app = kwargs.get("workspace_1_app", "")
            workspace_2_app = kwargs.get("workspace_2_app", "")
            workspace_3_app = kwargs.get("workspace_3_app", "")
            workspace_1_hotkey = kwargs.get("workspace_1_hotkey", "")
            workspace_2_hotkey = kwargs.get("workspace_2_hotkey", "")
            workspace_3_hotkey = kwargs.get("workspace_3_hotkey", "")
            custom_commands = json.dumps(kwargs.get("custom_commands", {}))
            urls = json.dumps(kwargs.get("urls", []))

            cursor.execute("""
                INSERT INTO projects
                (name, folder_path, zen_container, workspace_1_app,
                 workspace_2_app, workspace_3_app, workspace_1_hotkey,
                 workspace_2_hotkey, workspace_3_hotkey, custom_commands, urls)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, folder_path, zen_container, workspace_1_app,
                  workspace_2_app, workspace_3_app, workspace_1_hotkey,
                  workspace_2_hotkey, workspace_3_hotkey, custom_commands, urls))

            project_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return project_id
        except sqlite3.IntegrityError:
            print(f"Erro: Projeto '{name}' ja existe")
            return None
        except Exception as e:
            print(f"Erro ao criar projeto: {e}")
            return None

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Retorna todos os projetos"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects ORDER BY last_opened DESC, name ASC")
        rows = cursor.fetchall()
        conn.close()

        projects = []
        for row in rows:
            project = dict(row)
            # Converter JSON strings de volta para objetos
            if project.get("custom_commands"):
                project["custom_commands"] = json.loads(project["custom_commands"])
            if project.get("urls"):
                project["urls"] = json.loads(project["urls"])
            projects.append(project)

        return projects

    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Retorna um projeto pelo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            project = dict(row)
            if project.get("custom_commands"):
                project["custom_commands"] = json.loads(project["custom_commands"])
            if project.get("urls"):
                project["urls"] = json.loads(project["urls"])
            return project

        return None

    def get_active_project(self) -> Optional[Dict[str, Any]]:
        """Retorna o projeto ativo atual"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM projects WHERE is_active = 1 LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            project = dict(row)
            if project.get("custom_commands"):
                project["custom_commands"] = json.loads(project["custom_commands"])
            if project.get("urls"):
                project["urls"] = json.loads(project["urls"])
            return project

        return None

    def update_project(self, project_id: int, **kwargs) -> bool:
        """Atualiza um projeto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Campos atualizaveis
            updates = []
            values = []

            for field in ["name", "folder_path", "zen_container",
                         "workspace_1_app", "workspace_2_app", "workspace_3_app",
                         "workspace_1_hotkey", "workspace_2_hotkey", "workspace_3_hotkey"]:
                if field in kwargs:
                    updates.append(f"{field} = ?")
                    values.append(kwargs[field])

            if "custom_commands" in kwargs:
                updates.append("custom_commands = ?")
                values.append(json.dumps(kwargs["custom_commands"]))

            if "urls" in kwargs:
                updates.append("urls = ?")
                values.append(json.dumps(kwargs["urls"]))

            if not updates:
                return False

            values.append(project_id)
            query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, values)
            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Erro ao atualizar projeto: {e}")
            return False

    def delete_project(self, project_id: int) -> bool:
        """Deleta um projeto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Erro ao deletar projeto: {e}")
            return False

    def set_active_project(self, project_id: int) -> bool:
        """Define um projeto como ativo (e desativa todos os outros)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Desativar todos os projetos
            cursor.execute("UPDATE projects SET is_active = 0")

            # Ativar o projeto especificado
            cursor.execute(
                "UPDATE projects SET is_active = 1, last_opened = ? WHERE id = ?",
                (datetime.now().isoformat(), project_id)
            )

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Erro ao definir projeto ativo: {e}")
            return False

    def deactivate_all_projects(self) -> bool:
        """Desativa todos os projetos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("UPDATE projects SET is_active = 0")

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Erro ao desativar projetos: {e}")
            return False


# Teste basico
if __name__ == "__main__":
    db = Database("test_projects.db")

    # Criar projeto de teste
    project_id = db.create_project(
        name="Teste Projeto",
        folder_path="/home/user/projects/teste",
        zen_container="Work",
        workspace_1_app="zed",
        workspace_2_app="zen-browser",
        workspace_3_app="terminal",
        urls=["http://localhost:3000", "https://vercel.com"]
    )

    print(f"Projeto criado com ID: {project_id}")

    # Listar todos os projetos
    projects = db.get_all_projects()
    print(f"Total de projetos: {len(projects)}")
    for p in projects:
        print(f"  - {p['name']} ({p['folder_path']})")
