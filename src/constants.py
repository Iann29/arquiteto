#!/usr/bin/env python3
"""
Constants - Configuracoes globais do Arquiteto
"""

# ============================================================================
# APPS E WORKSPACES
# ============================================================================

# Apps disponiveis para workspaces
AVAILABLE_APPS = [
    "",              # Vazio (nenhum app)
    "zed",           # Zed editor
    "cursor",        # Cursor editor
    "claude-code",   # Alias para Cursor
    "zen-browser",   # Zen Browser
    "zen",           # Alias para Zen Browser
    "terminal",      # Terminal (alias para ghostty)
    "ghostty",       # Ghostty terminal
    "kitty",         # Kitty terminal
    "alacritty",     # Alacritty terminal
]

# Mapeamento de aliases
APP_ALIASES = {
    "claude-code": "cursor",
    "terminal": "ghostty",
    "zen": "zen-browser",
}

# Descrição dos apps para a UI
APP_DESCRIPTIONS = {
    "zed": "Zed - Editor de código",
    "cursor": "Cursor - Editor AI",
    "claude-code": "Claude Code (alias para Cursor)",
    "zen-browser": "Zen Browser",
    "zen": "Zen Browser",
    "terminal": "Terminal (alias para Ghostty)",
    "ghostty": "Ghostty Terminal",
    "kitty": "Kitty Terminal",
    "alacritty": "Alacritty Terminal",
}

# ============================================================================
# UI CONSTANTS
# ============================================================================

# Janela principal
WINDOW_TITLE = "Arquiteto - Gerenciador de Projetos"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Layout do Map
MAP_SIDEBAR_WIDTH = 300
MAP_FOOTER_HEIGHT = 50

# Tamanhos de cards
CARD_SIZE_NODES = 100
CARD_SIZE_PROGRAMS = 80

# Tamanhos de imagens nos nodes
NODE_IMAGE_SIZE_DEFAULT = (60, 60)
NODE_IMAGE_SIZE_ABRIR = (70, 70)

# Cores dos cards (RGB)
CARD_COLOR_PROJETO_INICIADO = (100, 150, 255)
CARD_COLOR_ABRIR = (150, 255, 150)
CARD_COLOR_ZED = (70, 130, 255)
CARD_COLOR_CLAUDE = (217, 119, 87)

# Cores de texto
TEXT_COLOR_LIGHT = (220, 220, 220)
TEXT_COLOR_MEDIUM = (200, 200, 200)
TEXT_COLOR_DARK = (150, 150, 150)
TEXT_COLOR_COORDS = (100, 200, 255)
