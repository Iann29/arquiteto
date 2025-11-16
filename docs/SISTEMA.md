# 🖥️ Sistema PC - omarchy

## 📊 Sistema Base
- **Hostname:** omarchy
- **Distro:** Arch Linux (rolling release)
- **Kernel:** 6.17.7-arch1-1
- **Arquitetura:** x86_64 (64-bit)
- **Uptime:** 4 horas, 24 minutos
- **Tipo:** Notebook (bateria 100%)

## 🔧 Hardware
### Processador
- **CPU:** AMD Ryzen 7 5800H with Radeon Graphics
- **Cores:** 8 cores / 16 threads
- **Frequência:** 403 MHz - 4465 MHz (Boost habilitado)
- **Cache:** L3 cache com suporte a CAT

### Memória
- **RAM Total:** 16 GB
- **RAM Usada:** 10 GB (62%)
- **RAM Livre:** 2.2 GB
- **RAM Disponível:** 5.4 GB
- **Swap:** 4.0 GB (3.6 GB usado - 90%)

### Armazenamento
- **Disco:** 475 GB (LVM - /dev/mapper/root)
- **Usado:** 139 GB (30%)
- **Livre:** 335 GB
- **Partição:** / e /home no mesmo volume

### GPU
- **Placa de Vídeo:** NVIDIA GeForce RTX 3050 Mobile (GA107BM)
- **Driver NVIDIA:** 580.105.08
- **Arquitetura:** Ampere (rev a1)

## 🎨 Interface Gráfica

### Window Manager
- **WM:** Hyprland 0.52.1-1 (Wayland compositor)
- **Display Manager:** SDDM (Simple Desktop Display Manager)
- **Sessão:** Wayland
- **Bar:** Waybar 0.14.0-4

### Ferramentas Hyprland
- **hypridle** 0.1.7-4 (gerenciador de idle)
- **hyprlock** 0.9.2-4 (lock screen)
- **hyprpaper** 0.7.6-2 (wallpaper)
- **hyprpicker** 0.4.5-7 (color picker)
- **hyprshade** 4.0.0-1 (filtro de tela)
- **hyprshot** 1.3.0-4 (screenshots)
- **hyprsunset** 0.3.3-3 (redshift/night mode)
- **swaybg** 1.2.1-1 (background alternativo)

### Notificações e Extras
- **Notificações:** Mako 1.10.0-1
- **Terminal:** Alacritty 0.16.1-1 + Kitty (backup) + Ghostty
- **Cursor:** Hyprcursor 0.1.13-2

## 🖥️ Displays e Workspaces

### Monitor 1: eDP-1 (Notebook) 🔥 PRIMÁRIO - Workspace 1
- **ID Hardware:** 2 (ID do kernel, não afeta workspaces)
- **Workspace Inicial:** **1** ✅ (configurado via workspace rules)
- **Resolução:** 1920x1080 @ 120Hz
- **Posição:** 1536x0 (centro)
- **Fabricante:** BOE
- **Modelo:** 0x0A81
- **Tamanho Físico:** 340x190mm (15.6")
- **Escala:** 1.25
- **Transform:** 0 (landscape normal)
- **Status:** Ativo, **PRIMÁRIO** ✨
- **DPMS:** Ligado
- **VRR/FreeSync:** Desabilitado
- **Color Management:** sRGB
- **Workspaces Atribuídos:** 1, 4, 7 (padrão de rotação)

### Monitor 2: HDMI-A-1 (Gaming 240Hz) ⭐ - Workspace 2
- **ID Hardware:** 1
- **Workspace Inicial:** **2** ✅ (configurado via workspace rules)
- **Resolução:** 1920x1080 @ 240Hz (high refresh rate!)
- **Posição:** 0x0 (esquerda)
- **Fabricante:** Beihai Century Joint Innovation (Blizzard 27)
- **Modelo:** Blizzard 27 (27 polegadas)
- **Tamanho Físico:** 600x340mm
- **Escala:** 1.25
- **Transform:** 0 (landscape normal)
- **Status:** Ativo
- **DPMS:** Ligado
- **VRR/FreeSync:** Desabilitado
- **Modos Disponíveis:** 240Hz, 144Hz, 120Hz, 60Hz
- **Color Management:** sRGB
- **Workspaces Atribuídos:** 2, 5, 8 (padrão de rotação)

### Monitor 3: DP-2 (Vertical) 📱 - Workspace 3
- **ID Hardware:** 0
- **Workspace Inicial:** **3** ✅ (configurado via workspace rules)
- **Resolução:** 1920x1080 @ 60Hz (1080x1920 rotacionado)
- **Posição:** 3072x-1056 (direita, rotacionado)
- **Fabricante:** PZG HDMI
- **Tamanho Físico:** 600x330mm
- **Escala:** 1.00
- **Transform:** 1 (rotacionado 90° - portrait mode)
- **Status:** Ativo
- **DPMS:** Ligado
- **VRR/FreeSync:** Desabilitado
- **Color Management:** sRGB
- **Workspaces Atribuídos:** 3, 6, 9 (padrão de rotação)

### ✅ Configuração de Workspaces (CORRIGIDO!)

**Sistema:** Workspaces 1-9 são **DINÂMICOS** (podem ser movidos entre monitores com Super+Shift+número)

**Ordem Inicial Corrigida:**

| Workspace | Monitor Inicial | Descrição |
|-----------|----------------|-----------|
| **1** | **eDP-1 (Notebook)** ✅ | Workspace principal sempre no notebook |
| **2** | **HDMI-A-1 (Gaming)** ✅ | Segundo workspace no gaming |
| **3** | **DP-2 (Vertical)** ✅ | Terceiro workspace no vertical |
| 4 | eDP-1 (Notebook) | Quarto workspace volta pro notebook |
| 5 | HDMI-A-1 (Gaming) | Quinto no gaming |
| 6 | DP-2 (Vertical) | Sexto no vertical |
| 7 | eDP-1 (Notebook) | Sétimo no notebook |
| 8 | HDMI-A-1 (Gaming) | Oitavo no gaming |
| 9 | DP-2 (Vertical) | Nono no vertical |

**Atalhos:**
- **Ir para workspace:** Super+[1-9]
- **Mover janela:** Super+Shift+[1-9]

### Resumo dos Workspaces Ativos Agora

| Workspace | Monitor | Apps |
|-----------|---------|------|
| 1 | eDP-1 (Notebook) ✅ | Apps do notebook |
| 2 | HDMI-A-1 (Gaming) ✅ | Navegador/Gaming |
| 3 | DP-2 (Vertical) ✅ | Terminal/Código |

### Layout Físico dos Monitores
```
┌─────────────────────────────────────────────────┐
│                                                 │
│  [HDMI-A-1]        [eDP-1]         [DP-2]      │
│   Blizzard 27      Notebook         PZG        │
│   1920x1080        1920x1080      1080x1920    │
│   @ 240Hz          @ 120Hz         @ 60Hz      │
│   (0,0)            (1536,0)        (3072,-1056)│
│   Scale 1.25       Scale 1.25      Scale 1.0   │
│                                     (Vertical)  │
│   ┌─────────┐      ┌─────────┐     ┌───┐      │
│   │         │      │    ⭐   │     │   │      │
│   │ Gaming  │      │ FOCADO  │     │ V │      │
│   │         │      │         │     │ e │      │
│   │ 240Hz   │      │ 120Hz   │     │ r │      │
│   └─────────┘      └─────────┘     │ t │      │
│                                     │ . │      │
│                                     └───┘      │
└─────────────────────────────────────────────────┘

Total Resolução Virtual: 4992x2976 pixels
```

### Configuração Waybar
- **Reservado:** 26 pixels no topo (altura da barra)
- **Posição:** Top em todos os monitores

## 💻 Desenvolvimento

### Linguagens e Runtimes
- **Node.js:** v22.20.0
- **npm:** 10.9.3
- **Python:** 3.14.0
- **Rust:** 1.91.0

### Ferramentas Dev
- **Docker:** 28.5.2 (build ecc694264d)
- **Docker Compose:** 2.40.3
- **Docker Buildx:** 0.29.1
- **Git:** 2.51.2-2
- **GitHub CLI:** 2.83.0-1
- **LazyGit:** 0.56.0-1
- **LazyDocker:** 0.24.1-2

### Editores
- **Zed** principal
- **Claude Code:** 2.0.32-1
- **Vim:** 9.1.1841-1 (gvim)

### Navegadores
- **Google Chrome:** 142.0.7444.134-1 (principal)

## 🔌 Serviços Ativos (systemd)

### Principais
- **dbus-broker.service** - D-Bus System Message Bus
- **docker.service** - Docker Application Container Engine
- **containerd.service** - containerd container runtime
- **sddm.service** - Simple Desktop Display Manager
- **systemd-networkd.service** - Network Configuration
- **systemd-resolved.service** - DNS Resolution

### Conectividade
- **iwd.service** - Wireless service (WiFi Intel)
- **avahi-daemon.service** - mDNS/DNS-SD Stack
- **bluetooth.service** - Bluetooth service

### Sistema
- **polkit.service** - Authorization Manager
- **rtkit-daemon.service** - RealtimeKit (audio realtime)
- **power-profiles-daemon.service** - Power Management
- **udisks2.service** - Disk Manager
- **upower.service** - Battery/Power daemon

### Impressão
- **cups.service** - CUPS Scheduler
- **cups-browsed.service** - Remote CUPS printers

### Extras
- **limine-snapper-sync.service** - Snapper snapshots sync

## 📦 Pacotes

### Estatísticas
- **Total instalado:** 1329 pacotes
- **Gerenciador:** pacman + AUR helpers

### Categorias Principais
- Hyprland ecosystem (16 pacotes)
- Docker stack (3 pacotes)
- Dev tools (Git, GitHub CLI, Lazy*)
- Editores (Cursor, Claude Code, Vim)
- Navegadores (Chrome)
- Linguagens (Node, Python, Rust)

## 🌐 Rede
- **Gerenciador:** systemd-networkd + iwd (WiFi)
- **DNS:** systemd-resolved
- **mDNS:** Avahi daemon

## 📁 Estrutura de Configuração
```
~/.config/
├── hypr/          (config Hyprland - 832 bytes)
├── waybar/        (config Waybar - 144 bytes)
├── alacritty/     (config terminal)
├── kitty/         (config terminal backup)
└── mako/          (config notificações)
```

## 🔋 Performance Atual
- **CPU:** Uso variável (8 cores disponíveis)
- **RAM:** 62% usado (10GB/16GB)
- **Swap:** 90% usado (alerta: considerar aumentar RAM ativa)
- **Disco:** 30% usado (335GB livres)
- **Bateria:** 100% (carregado)
- **Uptime:** ~4 horas

## 🛠️ Shell
- **Shell Padrão:** Bash (/usr/bin/bash)
- **Tipo Sessão:** Wayland (XDG_SESSION_TYPE)

## ⚠️ Observações
1. **Swap alto:** 90% de uso do swap indica que pode estar faltando RAM em certos momentos
2. **Hyprland:** Versão recente (0.52.1) com todo ecossistema instalado
3. **NVIDIA:** Driver proprietário atualizado (580.105.08)
4. **Docker:** Instalação completa com Compose e Buildx
5. **Node.js:** Versão 22 LTS (muito recente)
6. **Python:** Versão 3.14.0 (bleeding edge)
7. **Arch Linux:** Rolling release, sempre atualizado
