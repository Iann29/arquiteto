# 🏗️ Arquiteto

Visual workflow automation tool for Hyprland.

## 📋 About

Arquiteto is a visual automation system that lets you configure and execute complex workflows through a node-based graphical interface. Configure once, execute always!

Built and tested on **Hyprland with Omarchy**.

## 🚀 Features

- **Node-based visual editor** with DearPyGUI
- **Workflow automation** through visual node connections
- **Hyprland integration** (workspaces and applications)
- **Project management** with SQLite database
- **Focus control** (Zen mode)
- **System monitoring** (RAM and resources)

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🏃 Usage

```bash
# Method 1: Run script
./run.sh

# Method 2: Direct execution
cd src && python main.py
```

## 📖 Documentation

- [📝 System Concept](docs/CONCEITO.md) - Understand the idea behind Arquiteto (PT-BR)
- [🗺️ Planning](docs/PLANEJAMENTO.md) - Roadmap and planned features (PT-BR)
- [💻 System Specs](docs/SISTEMA.md) - Operating system information (PT-BR)

## 🏗️ Project Structure

```
arquiteto/
├── src/              # Python source code
├── assets/nodes/     # Node images and visual resources
├── docs/             # Project documentation
├── data/             # SQLite database
└── logs/             # Execution logs
```

## 🛠️ Technologies

- **Python 3.x**
- **DearPyGUI** - Graphical interface
- **SQLite** - Database
- **Hyprland** - Window manager (Wayland)

## 📊 Project Status

🚧 **Active development**

Currently implementing:
- ✅ Visual node editor
- ✅ Sidebar with clickable cards
- 🔄 Workflow execution system
- 🔄 Node library (applications, services, actions)

## 💡 How It Works

Arquiteto lets you visually build what should happen when starting a project:

```
[Project Started] → [Open] → [Code Editor]
                           ↓
                       [Terminal]
                       [Services]
```

When executing this workflow, the system automatically:
1. Initializes your project
2. Opens your code editor
3. Opens a terminal
4. Starts required services

All with one click! 🚀

## 📝 License

This project is for personal use.

## 👤 Author

Ian Bee
