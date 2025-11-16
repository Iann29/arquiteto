#!/bin/bash
# Script para rodar o Arquiteto com configurações otimizadas para Wayland/Hyprland

# Força uso de Wayland (se disponível)
export SDL_VIDEODRIVER=wayland
export _JAVA_AWT_WM_NONREPARENTING=1
export QT_QPA_PLATFORM=wayland
export GDK_BACKEND=wayland

# Ativa venv e roda
source venv/bin/activate
cd src && python main.py
