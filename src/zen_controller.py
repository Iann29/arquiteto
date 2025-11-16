#!/usr/bin/env python3
"""
Zen Controller - Controle do navegador Zen
NOTA: Zen browser nao possui CLI nativa para containers.
Esta implementacao usa subprocess para abrir o Zen de forma basica.
Para controle avancado de containers, seria necessario Selenium/Playwright.
"""

import subprocess
import time
import json
import configparser
from pathlib import Path
from typing import List, Optional


class ZenController:
    def __init__(self, zen_binary: str = "zen-browser"):
        self.zen_binary = zen_binary

    def is_zen_installed(self) -> bool:
        """Verifica se o Zen esta instalado"""
        try:
            result = subprocess.run(
                ["which", self.zen_binary],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except:
            return False

    def open_zen(self, urls: Optional[List[str]] = None, new_window: bool = False):
        """
        Abre o Zen browser

        Args:
            urls: Lista de URLs para abrir
            new_window: Se True, abre em nova janela
        """
        if not self.is_zen_installed():
            print(f"Erro: {self.zen_binary} nao encontrado no sistema")
            return False

        try:
            command = [self.zen_binary]

            if new_window:
                command.append("--new-window")

            if urls:
                command.extend(urls)

            # Abrir Zen em background
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            return True
        except Exception as e:
            print(f"Erro ao abrir Zen: {e}")
            return False

    def open_url_in_new_tab(self, url: str):
        """Abre URL em nova aba (Zen ja deve estar rodando)"""
        try:
            subprocess.Popen(
                [self.zen_binary, "--new-tab", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except Exception as e:
            print(f"Erro ao abrir URL: {e}")
            return False

    def close_all_zen_instances(self):
        """Fecha todas as instancias do Zen"""
        try:
            subprocess.run(["pkill", "-9", "zen-browser"], capture_output=True, timeout=2)
            time.sleep(0.2)
            return True
        except Exception as e:
            print(f"Erro ao fechar Zen: {e}")
            return False

    def open_container(self, container_name: str, urls: Optional[List[str]] = None):
        """
        Abre Zen Browser

        NOTA: Zen Browser nao suporta abertura em workspace/espaco especifico via CLI.
        O parametro container_name e mantido apenas como referencia (nao e utilizado).
        Usuario deve trocar workspace manualmente apos abrir o Zen.
        """
        if not self.is_zen_installed():
            print(f"Erro: {self.zen_binary} nao encontrado")
            return False

        try:
            # Abrir Zen normalmente
            print(f"Abrindo Zen Browser...")
            if container_name:
                print(f"[INFO] Workspace/Espaco '{container_name}' deve ser trocado manualmente")

            return self.open_zen(urls=urls)

        except Exception as e:
            print(f"Erro ao abrir Zen: {e}")
            return False

    def find_zen_profile_path(self) -> Optional[Path]:
        """Encontra automaticamente o path do profile ativo do Zen"""
        # Detecta se e instalacao Flatpak ou normal
        zen_base = Path.home() / ".zen"
        flatpak_base = Path.home() / ".var/app/app.zen_browser.zen/.zen"

        if flatpak_base.exists():
            zen_base = flatpak_base
        elif not zen_base.exists():
            return None

        profiles_ini = zen_base / "profiles.ini"
        if not profiles_ini.exists():
            return None

        # Parse do profiles.ini
        config = configparser.ConfigParser()
        config.read(profiles_ini)

        # Metodo 1: Secao Install* indica o profile em uso
        for section in config.sections():
            if section.startswith('Install'):
                profile_path = config.get(section, 'Default', fallback=None)
                if profile_path:
                    full_path = zen_base / profile_path
                    if full_path.exists():
                        return full_path

        # Metodo 2: Profile marcado como Default=1
        for section in config.sections():
            if config.get(section, 'Default', fallback='') == '1':
                profile_path = config.get(section, 'Path', fallback=None)
                if profile_path:
                    full_path = zen_base / profile_path
                    if full_path.exists():
                        return full_path

        # Metodo 3: Fallback - procura qualquer profile com containers.json
        for item in zen_base.iterdir():
            if item.is_dir() and (item / "containers.json").exists():
                return item

        return None

    def list_containers(self) -> List[str]:
        """Lista containers REAIS criados pelo usuario no Zen"""
        # Containers padroes como fallback
        default_containers = ["Default", "Personal", "Work", "Banking", "Shopping"]

        profile_path = self.find_zen_profile_path()

        if not profile_path:
            return default_containers

        containers_file = profile_path / "containers.json"

        if not containers_file.exists():
            return default_containers

        try:
            with open(containers_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extrair containers publicos (criados pelo usuario)
            containers = []
            for identity in data.get('identities', []):
                # Ignorar containers internos do sistema
                if not identity.get('public', False):
                    continue

                # Extrair nome (custom name ou l10nId traduzido)
                name = identity.get('name')
                if not name:
                    l10n_id = identity.get('l10nId', '')
                    name = l10n_id.replace('user-context-', '').title()

                if name:
                    containers.append(name)

            # Adicionar "Default" como primeira opcao e ordenar o resto
            containers = ["Default"] + sorted(containers)

            return containers if containers else default_containers

        except Exception as e:
            print(f"Erro ao ler containers do Zen: {e}")
            return default_containers


# Teste basico
if __name__ == "__main__":
    zc = ZenController()

    print("=== Teste Zen Controller ===\n")

    # Verificar instalacao
    if zc.is_zen_installed():
        print("✓ Zen browser encontrado")
    else:
        print("✗ Zen browser NAO encontrado")
        exit(1)

    # Listar containers
    print("\n=== Containers Disponiveis ===")
    containers = zc.list_containers()
    for i, container in enumerate(containers, 1):
        print(f"{i}. {container}")

    # Teste de abertura (comentado para nao abrir automaticamente)
    # print("\n=== Teste de Abertura ===")
    # print("Abrindo Zen com URLs de teste...")
    # zc.open_zen(urls=["https://example.com", "https://github.com"])
    # print("Zen aberto!")

    print("\n[NOTA] Para controle avancado de containers, e necessario:")
    print("  1. Instalar geckodriver: pacman -S geckodriver")
    print("  2. Implementar ZenControllerAdvanced com Selenium")
    print("  3. Ou usar script firefox-container adaptado para Zen")
