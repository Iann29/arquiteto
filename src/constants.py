#!/usr/bin/env python3
"""
Constants - Configuracoes globais do Arquiteto
"""

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
