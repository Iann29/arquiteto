#!/usr/bin/env python3
"""
Texture Manager - Gerenciamento centralizado de texturas DearPyGUI
"""

import os
import dearpygui.dearpygui as dpg
from pathlib import Path


class TextureManager:
    """Gerencia carregamento e cache de texturas"""

    _textures_loaded = False
    _texture_registry_tag = "texture_registry"

    @classmethod
    def load_all_textures(cls):
        """Carrega todas as texturas necessárias"""
        if cls._textures_loaded:
            return

        # Criar texture registry se não existir
        if not dpg.does_item_exist(cls._texture_registry_tag):
            dpg.add_texture_registry(tag=cls._texture_registry_tag)

        # Caminho base para imagens
        project_root = Path(__file__).parent.parent.parent
        nodes_path = project_root / "assets" / "nodes"
        apps_path = project_root / "assets" / "apps"

        # Carregar texturas de nodes
        cls._load_texture(nodes_path / "projeto_iniciado.png", "tex_projeto_iniciado")
        cls._load_texture(nodes_path / "abrir.png", "tex_abrir")
        cls._load_texture(nodes_path / "nodes_disponiveis.png", "tex_workspace")

        # Carregar texturas de apps
        cls._load_texture(apps_path / "zed-logo.png", "tex_zed")
        cls._load_texture(apps_path / "claude-ai-icon.png", "tex_claude")
        cls._load_texture(apps_path / "zen-browser.png", "tex_zen")
        cls._load_texture(apps_path / "google.png", "tex_google")

        cls._textures_loaded = True
        print("[TextureManager] Todas as texturas carregadas")

    @classmethod
    def _load_texture(cls, path: Path, tag: str):
        """
        Carrega uma textura individual

        Args:
            path: Path para a imagem
            tag: Tag da textura no registry
        """
        if not path.exists():
            print(f"[TextureManager] AVISO: Textura não encontrada: {path}")
            return

        try:
            width, height, channels, data = dpg.load_image(str(path))
            dpg.add_static_texture(
                width=width,
                height=height,
                default_value=data,
                tag=tag,
                parent=cls._texture_registry_tag,
            )
            print(f"[TextureManager] Textura carregada: {path.name} ({width}x{height})")
        except Exception as e:
            print(f"[TextureManager] Erro ao carregar {path}: {e}")

    @classmethod
    def texture_exists(cls, tag: str) -> bool:
        """Verifica se uma textura existe"""
        return dpg.does_item_exist(tag)

    @classmethod
    def get_texture(cls, tag: str):
        """Retorna o tag da textura (para uso em add_image)"""
        if cls.texture_exists(tag):
            return tag
        return None
