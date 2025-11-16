#!/usr/bin/env python3
"""
Workspace Manager - Gerenciamento de workspaces do Hyprland
"""

import subprocess
import json
from typing import List, Dict, Optional, Any


class WorkspaceManager:
    def __init__(self):
        pass

    def get_all_workspaces(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os workspaces"""
        try:
            result = subprocess.run(
                ["hyprctl", "workspaces", "-j"],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Erro ao obter workspaces: {e}")

        return []

    def get_workspace_info(self, workspace_id: int) -> Optional[Dict[str, Any]]:
        """Retorna informacoes de um workspace especifico"""
        workspaces = self.get_all_workspaces()
        for ws in workspaces:
            if ws.get("id") == workspace_id:
                return ws
        return None

    def get_active_workspace(self) -> Optional[Dict[str, Any]]:
        """Retorna o workspace ativo"""
        try:
            result = subprocess.run(
                ["hyprctl", "activeworkspace", "-j"],
                capture_output=True,
                text=True,
                timeout=1
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"Erro ao obter workspace ativo: {e}")

        return None

    def switch_to_workspace(self, workspace_id: int) -> bool:
        """Muda para um workspace especifico"""
        try:
            result = subprocess.run(
                ["hyprctl", "dispatch", "workspace", str(workspace_id)],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Erro ao mudar para workspace {workspace_id}: {e}")
            return False

    def get_windows_in_workspace(self, workspace_id: int) -> List[Dict[str, Any]]:
        """Retorna todas as janelas em um workspace"""
        windows = []
        try:
            result = subprocess.run(
                ["hyprctl", "clients", "-j"],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                clients = json.loads(result.stdout)
                for client in clients:
                    ws = client.get("workspace", {})
                    if ws.get("id") == workspace_id:
                        windows.append(client)
        except Exception as e:
            print(f"Erro ao obter janelas do workspace {workspace_id}: {e}")

        return windows

    def move_window_to_workspace(self, window_address: str, workspace_id: int, silent: bool = False) -> bool:
        """Move uma janela para um workspace"""
        try:
            command = "movetoworkspacesilent" if silent else "movetoworkspace"
            result = subprocess.run(
                ["hyprctl", "dispatch", command, f"{workspace_id},address:{window_address}"],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Erro ao mover janela para workspace {workspace_id}: {e}")
            return False

    def close_window(self, window_address: str) -> bool:
        """Fecha uma janela especifica"""
        try:
            result = subprocess.run(
                ["hyprctl", "dispatch", "closewindow", f"address:{window_address}"],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Erro ao fechar janela: {e}")
            return False

    def find_window_by_title(self, title_substring: str) -> Optional[Dict[str, Any]]:
        """Encontra uma janela pelo titulo"""
        try:
            result = subprocess.run(
                ["hyprctl", "clients", "-j"],
                capture_output=True,
                text=True,
                timeout=2
            )

            if result.returncode == 0:
                clients = json.loads(result.stdout)
                for client in clients:
                    title = client.get("title", "")
                    if title_substring.lower() in title.lower():
                        return client
        except Exception as e:
            print(f"Erro ao buscar janela: {e}")

        return None

    def focus_window(self, window_address: str) -> bool:
        """Foca em uma janela especifica"""
        try:
            result = subprocess.run(
                ["hyprctl", "dispatch", "focuswindow", f"address:{window_address}"],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Erro ao focar janela: {e}")
            return False

    def get_workspace_stats(self) -> Dict[str, Any]:
        """Retorna estatisticas dos workspaces"""
        workspaces = self.get_all_workspaces()

        stats = {
            "total_workspaces": len(workspaces),
            "workspaces": []
        }

        for ws in workspaces:
            ws_id = ws.get("id", 0)
            windows = self.get_windows_in_workspace(ws_id)

            stats["workspaces"].append({
                "id": ws_id,
                "name": ws.get("name", str(ws_id)),
                "windows_count": len(windows),
                "monitor": ws.get("monitor", "unknown")
            })

        return stats


# Teste basico
if __name__ == "__main__":
    wm = WorkspaceManager()

    print("=== Workspace Ativo ===")
    active = wm.get_active_workspace()
    if active:
        print(f"ID: {active.get('id')}, Nome: {active.get('name')}")

    print("\n=== Estatisticas ===")
    stats = wm.get_workspace_stats()
    print(f"Total de workspaces: {stats['total_workspaces']}")
    for ws in stats['workspaces']:
        print(f"  WS {ws['id']}: {ws['windows_count']} janelas")

    print("\n=== Buscando janela Arquiteto ===")
    arquiteto = wm.find_window_by_title("Arquiteto")
    if arquiteto:
        print(f"Encontrado: {arquiteto.get('title')}")
        print(f"Workspace: {arquiteto.get('workspace', {}).get('id')}")
