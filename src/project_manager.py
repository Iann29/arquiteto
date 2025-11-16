#!/usr/bin/env python3
"""
Project Manager - Gerenciamento de abertura/fechamento de projetos
"""

import subprocess
import time
import psutil
from typing import Optional, Dict, Any, List
from database import Database


class ProjectManager:
    def __init__(self, db: Database):
        self.db = db

    def get_process_by_name(self, name: str) -> List[psutil.Process]:
        """Retorna lista de processos por nome"""
        processes = []
        for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
            try:
                proc_name = proc.info['name'].lower() if proc.info['name'] else ""
                if name.lower() in proc_name:
                    processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes

    def kill_processes(self, process_names: List[str]):
        """Mata processos por nome"""
        for name in process_names:
            try:
                # Primeiro tenta pkill (mais rapido)
                subprocess.run(["pkill", "-9", name], capture_output=True, timeout=2)
                time.sleep(0.1)
            except:
                pass

            # Depois verifica se ainda existem processos e mata via psutil
            processes = self.get_process_by_name(name)
            for proc in processes:
                try:
                    proc.kill()
                except:
                    pass

    def close_all_windows_in_workspace(self, workspace_id: int):
        """Fecha todas as janelas de um workspace especifico"""
        try:
            result = subprocess.run(
                ["hyprctl", "clients", "-j"],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                import json
                clients = json.loads(result.stdout)

                for client in clients:
                    ws = client.get("workspace", {})
                    if ws.get("id") == workspace_id:
                        address = client.get("address", "")
                        if address:
                            subprocess.run(
                                ["hyprctl", "dispatch", "closewindow", f"address:{address}"],
                                capture_output=True,
                                timeout=1
                            )
                            time.sleep(0.05)
        except Exception as e:
            print(f"Erro ao fechar janelas do workspace {workspace_id}: {e}")

    def parse_hotkey(self, hotkey_string: str) -> Optional[List[str]]:
        """
        Converte string de atalho em comando wtype

        Exemplos:
            "ctrl+shift+e" → ["wtype", "-M", "ctrl", "-M", "shift", "-P", "e", "-m", "shift", "-m", "ctrl"]
            "ctrl+alt+minus" → ["wtype", "-M", "ctrl", "-M", "alt", "-P", "minus", "-m", "alt", "-m", "ctrl"]

        Returns:
            Lista de argumentos para subprocess.run() ou None se inválido
        """
        if not hotkey_string or not hotkey_string.strip():
            return None

        # Normalizar: lowercase e remover espaços
        hotkey = hotkey_string.strip().lower()

        # Separar modificadores + tecla
        parts = hotkey.split("+")
        if len(parts) < 2:
            print(f"AVISO: Atalho inválido '{hotkey_string}' (precisa de pelo menos um modificador)")
            return None

        # Mapa de teclas especiais
        special_keys = {
            "-": "minus",
            "+": "plus",
            ",": "comma",
            ".": "period",
            "/": "slash",
            "\\": "backslash",
            "[": "bracketleft",
            "]": "bracketright",
            ";": "semicolon",
            "'": "apostrophe",
            "`": "grave",
            "=": "equal",
            "tab": "tab",
            "enter": "return",
            "esc": "escape",
            "space": "space",
            "backspace": "backspace",
            "delete": "delete",
        }

        # Modificadores válidos
        valid_modifiers = ["ctrl", "shift", "alt", "super", "meta"]

        modifiers = []
        key = None

        for i, part in enumerate(parts):
            part = part.strip()

            # Última parte é a tecla principal
            if i == len(parts) - 1:
                # Traduzir tecla especial se necessário
                key = special_keys.get(part, part)
            else:
                # Validar modificador
                if part not in valid_modifiers:
                    print(f"AVISO: Modificador inválido '{part}' em '{hotkey_string}'")
                    return None
                modifiers.append(part)

        if not key or not modifiers:
            print(f"AVISO: Atalho malformado '{hotkey_string}'")
            return None

        # Construir comando wtype
        # Formato: wtype -M mod1 -M mod2 -P key -m mod2 -m mod1
        cmd = ["wtype"]

        # Pressionar modificadores (ordem crescente)
        for mod in modifiers:
            cmd.extend(["-M", mod])

        # Pressionar tecla principal
        cmd.extend(["-P", key])

        # Soltar modificadores (ordem reversa)
        for mod in reversed(modifiers):
            cmd.extend(["-m", mod])

        return cmd

    def send_hotkey(self, window_address: str, hotkey_string: str, delay_before: float = 0.5, delay_after: float = 0.3) -> bool:
        """
        Envia atalho de teclado para uma janela específica

        Args:
            window_address: Endereço da janela (hyprctl)
            hotkey_string: String do atalho (ex: "ctrl+shift+e")
            delay_before: Delay antes de enviar (para janela estabilizar)
            delay_after: Delay após enviar

        Returns:
            bool: True se sucesso, False se erro
        """
        if not hotkey_string or not hotkey_string.strip():
            return False

        # Parsear atalho
        cmd = self.parse_hotkey(hotkey_string)
        if not cmd:
            return False

        try:
            # Aguardar janela estabilizar
            time.sleep(delay_before)

            # Focar a janela
            subprocess.run(
                ["hyprctl", "dispatch", "focuswindow", f"address:{window_address}"],
                capture_output=True,
                timeout=1
            )
            time.sleep(0.2)

            # Enviar atalho via wtype
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=1
            )

            if result.returncode == 0:
                print(f"Atalho '{hotkey_string}' enviado com sucesso")
                time.sleep(delay_after)
                return True
            else:
                stderr = result.stderr.decode() if result.stderr else ""
                print(f"Erro ao enviar atalho '{hotkey_string}': {stderr}")
                return False

        except FileNotFoundError:
            print("ERRO: wtype não encontrado! Instale com: sudo pacman -S wtype")
            return False
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT ao enviar atalho '{hotkey_string}'")
            return False
        except Exception as e:
            print(f"Erro inesperado ao enviar atalho '{hotkey_string}': {e}")
            return False

    def open_claude_code_in_terminal(self, workspace_id: int, folder_path: str):
        """Abre Claude Code via terminal (ghostty) no diretório do projeto"""
        try:
            print(f"[DEBUG] Claude Code: folder_path = '{folder_path}'")

            # 1. Ir para o workspace
            subprocess.run(
                ["hyprctl", "dispatch", "workspace", str(workspace_id)],
                capture_output=True,
                timeout=1
            )

            time.sleep(0.2)

            # 2. Abrir ghostty no diretório do projeto E executar "claude" diretamente
            # Ghostty aceita -e para executar comando
            # Usamos bash -c para executar "claude" no diretório correto
            subprocess.Popen(
                [
                    "ghostty",
                    f"--working-directory={folder_path}",
                    "-e", "bash", "-c", "claude"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            print(f"Claude Code iniciado via terminal no WS{workspace_id}")
            return True

        except Exception as e:
            print(f"Erro ao abrir Claude Code via terminal: {e}")
            return False

    def open_app_in_workspace(self, app_name: str, workspace_id: int, folder_path: Optional[str] = None, zen_container: Optional[str] = None, hotkey: Optional[str] = None):
        """Abre um app em um workspace especifico e opcionalmente envia atalho de teclado"""
        try:
            # Primeiro vai para o workspace
            subprocess.run(
                ["hyprctl", "dispatch", "workspace", str(workspace_id)],
                capture_output=True,
                timeout=1
            )

            time.sleep(0.2)

            # Se é Zen, usar ZenController com container
            if app_name.lower() in ["zen-browser", "zen"]:
                from zen_controller import ZenController
                zen = ZenController()
                if zen_container:
                    zen.open_container(zen_container)
                else:
                    zen.open_zen()
                time.sleep(0.3)
                return True

            # Se é Claude Code, abrir via terminal com comando "claude"
            if app_name.lower() == "claude-code":
                if folder_path:
                    return self.open_claude_code_in_terminal(workspace_id, folder_path)
                else:
                    print("AVISO: Claude Code precisa de folder_path para abrir")
                    return False

            # Mapa de apps para comandos (SEM folder_path aqui)
            app_commands = {
                "zed": ["zeditor"],  # Zed no Arch é "zeditor", não "zed"
                "terminal": ["ghostty"],
                "ghostty": ["ghostty"],
                "kitty": ["kitty"],
                "alacritty": ["alacritty"],
                "cursor": ["cursor"],
                # "claude-code" é tratado separadamente acima
            }

            command = app_commands.get(app_name.lower())
            if not command:
                print(f"App desconhecido: {app_name}")
                return False

            # Adicionar folder_path aos comandos se aplicavel
            if folder_path:
                if app_name.lower() in ["zed", "cursor"]:
                    # Zed/Cursor: folder_path como argumento
                    command = command + [folder_path]
                elif app_name.lower() == "ghostty":
                    # Ghostty: usar --working-directory
                    command = ["ghostty", "--working-directory", folder_path]
                elif app_name.lower() in ["kitty", "alacritty"]:
                    # Kitty/Alacritty: usar --directory
                    command = command + ["--directory", folder_path]

            # Abre o app
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            time.sleep(0.5)  # Aguardar app abrir

            # Garantir que Zed fique no workspace correto (Zed às vezes abre em workspace errado)
            if app_name.lower() == "zed":
                time.sleep(1.0)  # Zed precisa de mais tempo para carregar pasta
                try:
                    result = subprocess.run(
                        ["hyprctl", "clients", "-j"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0:
                        import json
                        clients = json.loads(result.stdout)
                        for client in clients:
                            if "zed" in client.get("class", "").lower():
                                # Se Zed está em outro workspace, mover
                                ws = client.get("workspace", {})
                                if ws.get("id") != workspace_id:
                                    address = client.get("address", "")
                                    subprocess.run(
                                        ["hyprctl", "dispatch", "movetoworkspacesilent", f"{workspace_id},address:{address}"],
                                        capture_output=True,
                                        timeout=1
                                    )
                                    print(f"Zed movido para workspace {workspace_id}")
                                break
                except Exception as e:
                    print(f"Aviso: Não consegui garantir Zed no workspace {workspace_id}: {e}")

            # Enviar hotkey se configurado (lógica genérica para qualquer app)
            if hotkey and hotkey.strip():
                time.sleep(0.5)  # Aguardar app carregar completamente

                try:
                    # Buscar endereço da janela recém-aberta
                    result = subprocess.run(
                        ["hyprctl", "clients", "-j"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )

                    if result.returncode == 0:
                        import json
                        clients = json.loads(result.stdout)

                        # Mapa de apps para class names
                        app_class_map = {
                            "zed": "zed",
                            "zen-browser": "zen",
                            "zen": "zen",
                            "terminal": "ghostty",
                            "ghostty": "ghostty",
                            "kitty": "kitty",
                            "cursor": "cursor",
                            "alacritty": "alacritty",
                            "claude-code": "ghostty",  # Claude Code roda em terminal
                        }

                        expected_class = app_class_map.get(app_name.lower(), "").lower()

                        # Encontrar janela do app no workspace correto
                        for client in clients:
                            ws = client.get("workspace", {})
                            if ws.get("id") == workspace_id:
                                class_name = client.get("class", "").lower()

                                # Verificar se é o app que acabamos de abrir
                                if expected_class and expected_class in class_name:
                                    address = client.get("address", "")
                                    if address:
                                        print(f"Enviando hotkey '{hotkey}' para {app_name}...")
                                        self.send_hotkey(address, hotkey)
                                    break
                except Exception as e:
                    print(f"Erro ao enviar hotkey para {app_name}: {e}")

            return True
        except Exception as e:
            print(f"Erro ao abrir {app_name} no workspace {workspace_id}: {e}")
            return False

    def close_project(self, project: Dict[str, Any]):
        """Fecha um projeto (mata processos e limpa workspaces)"""
        print(f"Fechando projeto: {project['name']}")

        # Lista de processos para matar
        processes_to_kill = []

        # Coletar nomes de apps dos workspaces
        for ws_num in [1, 2, 3]:
            app = project.get(f"workspace_{ws_num}_app")
            if app:
                processes_to_kill.append(app)

        # Apps padroes para matar
        default_apps = ["zed", "zen-browser", "cursor", "ghostty", "kitty", "alacritty"]
        for app in default_apps:
            if app not in processes_to_kill:
                processes_to_kill.append(app)

        # Matar processos
        print(f"Matando processos: {', '.join(processes_to_kill)}")
        self.kill_processes(processes_to_kill)

        # Aguardar processos morrerem
        time.sleep(0.5)

        # Fechar janelas restantes nos workspaces 1, 2, 3
        print("Limpando workspaces 1, 2, 3")
        for ws_id in [1, 2, 3]:
            self.close_all_windows_in_workspace(ws_id)
            time.sleep(0.1)

        print(f"Projeto '{project['name']}' fechado")

    def open_project(self, project: Dict[str, Any]):
        """Abre um projeto (distribui apps nos workspaces)"""
        print(f"Abrindo projeto: {project['name']}")

        folder_path = project.get("folder_path", "")
        zen_container = project.get("zen_container", "")

        # Abrir apps nos workspaces configurados
        for ws_num in [1, 2, 3]:
            app = project.get(f"workspace_{ws_num}_app")
            hotkey = project.get(f"workspace_{ws_num}_hotkey", "")  # Pegar hotkey configurado

            if app and app.strip():
                print(f"Abrindo {app} no workspace {ws_num}")

                # Passar folder_path para apps que usam diretorio
                folder = folder_path if app.lower() in ["zed", "cursor", "terminal", "ghostty", "kitty", "alacritty", "claude-code"] else None

                # Passar zen_container apenas para Zen
                zen_cont = zen_container if app.lower() in ["zen-browser", "zen"] else None

                self.open_app_in_workspace(app, ws_num, folder, zen_cont, hotkey)  # Passar hotkey
                time.sleep(0.3)

        print(f"Projeto '{project['name']}' aberto")

    def move_all_windows_to_ws5(self):
        """Move todas as janelas dos workspaces 1, 2, 3 para workspace 5 (preserva estado)"""
        try:
            import os
            import json

            # PID do processo atual (Arquiteto)
            arquiteto_pid = os.getpid()

            result = subprocess.run(
                ["hyprctl", "clients", "-j"],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                clients = json.loads(result.stdout)

                # Coletar todos os endereços primeiro (evita problemas com estado desatualizado)
                windows_to_move = []

                for client in clients:
                    ws = client.get("workspace", {})
                    ws_id = ws.get("id")

                    # Se janela está no workspace 1, 2 ou 3
                    if ws_id in [1, 2, 3]:
                        address = client.get("address", "")
                        title = client.get("title", "")
                        pid = client.get("pid", -1)

                        # NÃO mover se for o processo do Arquiteto (usa PID ao invés de título)
                        if pid != arquiteto_pid:
                            if address:
                                windows_to_move.append({
                                    "address": address,
                                    "title": title,
                                    "ws_id": ws_id,
                                    "pid": pid
                                })

                print(f"[DEBUG] PID Arquiteto: {arquiteto_pid}")
                print(f"Encontradas {len(windows_to_move)} janela(s) para mover para WS5")

                # Debug: mostrar janelas encontradas
                for w in windows_to_move:
                    print(f"  - WS{w['ws_id']}: {w['title']} (PID: {w['pid']})")

                # Agora mover todas as janelas coletadas
                moved_count = 0
                for window in windows_to_move:
                    try:
                        subprocess.run(
                            ["hyprctl", "dispatch", "movetoworkspacesilent", f"5,address:{window['address']}"],
                            capture_output=True,
                            timeout=1
                        )
                        moved_count += 1
                        print(f"Janela movida WS{window['ws_id']}→WS5: {window['title']}")
                        time.sleep(0.05)
                    except Exception as e:
                        print(f"Erro ao mover janela '{window['title']}': {e}")

                if moved_count > 0:
                    print(f"Total: {moved_count} janela(s) movida(s) para WS5")
                return True
        except Exception as e:
            print(f"Erro ao mover janelas para WS5: {e}")

        return False

    def move_arquiteto_to_workspace_9(self, arquiteto_window_title: str = "Arquiteto"):
        """Move a janela do Arquiteto para workspace 9 usando PID do processo"""
        try:
            import os
            import json

            # PID do processo atual (Arquiteto)
            arquiteto_pid = os.getpid()

            result = subprocess.run(
                ["hyprctl", "clients", "-j"],
                capture_output=True,
                text=True,
                timeout=1
            )

            if result.returncode == 0:
                clients = json.loads(result.stdout)

                for client in clients:
                    pid = client.get("pid", -1)

                    # Detecta pela PID (mais confiável que título)
                    if pid == arquiteto_pid:
                        address = client.get("address", "")
                        current_ws = client.get("workspace", {}).get("id")
                        title = client.get("title", "")

                        # Se já está em workspace 9, skip
                        if current_ws == 9:
                            print(f"Arquiteto já está em workspace 9")
                            return True

                        if address:
                            subprocess.run(
                                ["hyprctl", "dispatch", "movetoworkspacesilent", f"9,address:{address}"],
                                capture_output=True,
                                timeout=1
                            )
                            print(f"Arquiteto movido para workspace 9 (era WS{current_ws})")
                            return True
        except Exception as e:
            print(f"Erro ao mover Arquiteto para workspace 9: {e}")

        print("AVISO: Não consegui encontrar a janela do Arquiteto!")
        return False

    def switch_project(self, new_project_id: int):
        """Troca de projeto: preserva janelas antigas e organiza workspaces"""
        # 1. Pegar novo projeto
        new_project = self.db.get_project_by_id(new_project_id)
        if not new_project:
            print(f"Erro: Projeto {new_project_id} nao encontrado")
            return False

        print(f"Trocando para projeto: {new_project['name']}")

        # 2. Mover TODAS as janelas dos WS 1, 2, 3 para WS5 (preserva estado)
        print("Organizando workspaces: WS1,2,3 → WS5...")
        self.move_all_windows_to_ws5()
        time.sleep(0.3)

        # 3. Mover Arquiteto para workspace 9
        print("Movendo Arquiteto para WS9...")
        self.move_arquiteto_to_workspace_9()
        time.sleep(0.3)

        # 4. Abrir novo projeto nos workspaces limpos (1, 2, 3)
        print(f"Abrindo projeto '{new_project['name']}' em WS1,2,3...")
        self.open_project(new_project)

        # 5. Definir novo projeto como ativo
        self.db.set_active_project(new_project_id)

        # 6. Focar workspace 1 (onde o projeto foi aberto)
        time.sleep(0.5)
        subprocess.run(
            ["hyprctl", "dispatch", "workspace", "1"],
            capture_output=True,
            timeout=1
        )

        print(f"Projeto '{new_project['name']}' ativo!")
        return True

    def emergency_close_all(self):
        """EMERGENCIA: Fecha TUDO para liberar RAM"""
        print("EMERGENCIA: Fechando tudo!")

        # Lista de processos comuns
        processes = ["zed", "zen-browser", "cursor", "kitty", "alacritty", "code"]

        self.kill_processes(processes)

        # Limpar workspaces 1, 2, 3
        for ws_id in [1, 2, 3]:
            self.close_all_windows_in_workspace(ws_id)

        # Desativar todos os projetos
        self.db.deactivate_all_projects()

        print("Tudo fechado! RAM liberada.")


# Teste basico
if __name__ == "__main__":
    from database import Database

    db = Database("test_projects.db")
    pm = ProjectManager(db)

    # Criar projeto de teste
    project_id = db.create_project(
        name="Teste Switch",
        folder_path="/home/ian/Documents",
        workspace_1_app="zed",
        workspace_2_app="zen-browser",
        workspace_3_app="kitty"
    )

    print(f"Projeto criado: {project_id}")

    # Simular troca de projeto
    if project_id:
        input("Pressione Enter para abrir projeto...")
        pm.switch_project(project_id)

        input("Pressione Enter para fechar tudo (emergencia)...")
        pm.emergency_close_all()
