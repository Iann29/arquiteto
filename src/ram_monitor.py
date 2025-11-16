#!/usr/bin/env python3
"""
RAM Monitor - Monitoramento de RAM em tempo real
"""

import psutil
from typing import Dict, Any, Tuple


class RAMMonitor:
    def __init__(self):
        self.warning_threshold = 13.0  # GB
        self.critical_threshold = 14.5  # GB
        self.total_ram_gb = psutil.virtual_memory().total / (1024**3)

    def get_ram_info(self) -> Dict[str, Any]:
        """Retorna informacoes sobre uso de RAM"""
        mem = psutil.virtual_memory()

        return {
            "total_gb": self.total_ram_gb,
            "used_gb": mem.used / (1024**3),
            "available_gb": mem.available / (1024**3),
            "percent": mem.percent,
            "is_warning": mem.used / (1024**3) > self.warning_threshold,
            "is_critical": mem.used / (1024**3) > self.critical_threshold,
        }

    def get_ram_status(self) -> Tuple[str, Tuple[int, int, int]]:
        """
        Retorna status da RAM e cor RGB
        Returns: (status_text, (R, G, B))
        """
        info = self.get_ram_info()
        used_gb = info["used_gb"]
        percent = info["percent"]

        if info["is_critical"]:
            return (f"RAM CRITICA: {used_gb:.1f}GB / {self.total_ram_gb:.0f}GB ({percent:.0f}%)",
                    (255, 50, 50))  # Vermelho
        elif info["is_warning"]:
            return (f"RAM Alerta: {used_gb:.1f}GB / {self.total_ram_gb:.0f}GB ({percent:.0f}%)",
                    (255, 200, 0))  # Amarelo
        else:
            return (f"RAM: {used_gb:.1f}GB / {self.total_ram_gb:.0f}GB ({percent:.0f}%)",
                    (100, 255, 100))  # Verde

    def get_top_processes(self, limit: int = 10) -> list:
        """Retorna os processos que mais consomem RAM"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                mem_mb = proc.info['memory_info'].rss / (1024**2)
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory_mb': mem_mb
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Ordenar por memoria usada (decrescente)
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)

        return processes[:limit]

    def get_ram_percentage_for_plot(self) -> float:
        """Retorna porcentagem de RAM usada (0-100) para graficos"""
        return psutil.virtual_memory().percent

    def format_ram_for_display(self) -> str:
        """Retorna string formatada para display"""
        info = self.get_ram_info()
        return f"{info['used_gb']:.1f} / {info['total_gb']:.0f} GB ({info['percent']:.0f}%)"

    def should_show_warning(self) -> bool:
        """Retorna True se deve mostrar alerta visual"""
        info = self.get_ram_info()
        return info["is_warning"] or info["is_critical"]

    def should_show_critical_popup(self) -> bool:
        """Retorna True se deve mostrar popup critico"""
        info = self.get_ram_info()
        return info["is_critical"]


# Teste basico
if __name__ == "__main__":
    import time

    monitor = RAMMonitor()

    print("=== Monitoramento de RAM ===\n")

    for i in range(5):
        info = monitor.get_ram_info()
        status, color = monitor.get_ram_status()

        print(f"[{i+1}/5] {status}")
        print(f"  Total: {info['total_gb']:.2f} GB")
        print(f"  Usado: {info['used_gb']:.2f} GB")
        print(f"  Disponivel: {info['available_gb']:.2f} GB")
        print(f"  Porcentagem: {info['percent']:.1f}%")
        print(f"  Alerta: {info['is_warning']}")
        print(f"  Critico: {info['is_critical']}")
        print(f"  Cor RGB: {color}")
        print()

        if i < 4:
            time.sleep(1)

    print("\n=== Top 5 Processos (RAM) ===")
    top_procs = monitor.get_top_processes(5)
    for i, proc in enumerate(top_procs, 1):
        print(f"{i}. {proc['name']}: {proc['memory_mb']:.1f} MB (PID: {proc['pid']})")
