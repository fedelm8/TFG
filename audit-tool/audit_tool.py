import os
import importlib
import json
import sys
from datetime import datetime

# Verificar si el script se ejecuta con privilegios de root
def check_root():
    if os.geteuid() != 0:
        print("[ERROR] Este script debe ejecutarse con sudo o como root.")
        sys.exit(1)

# Definir rutas
def setup_directories():
    global MODULES_DIR, REPORTS_DIR, REPORT_FILE
    MODULES_DIR = os.path.join(os.path.dirname(__file__), "modules")
    REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    REPORT_FILE = os.path.join(REPORTS_DIR, f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")

# Ejecutar módulos en orden manualmente
def run_selected_modules():
    results = {}

    # 1️⃣ Ejecutar información del sistema primero
    print("[INFO] Ejecutando módulo: sys_info...\n")
    results["sys_info"] = importlib.import_module("modules.sys_info").run()

    # 2️⃣ Ejecutar auditoría del kernel
    print("[INFO] Ejecutando módulo: kernel...\n")
    results["kernel"] = importlib.import_module("modules.kernel").run()

    # 3 Ejecutar auditoría del memoria y procesos
    print("[INFO] Ejecutando módulo: Memoria y Procesos...\n")
    results["mem_process"] = importlib.import_module("modules.mem_process").run()

    # 4 Ejecutar auditoría de usuarios grupos y autenticacion
    print("[INFO] Ejecutando módulo: Usuarios Grupos y Autenticacion...\n")
    results["users_groups_auth"] = importlib.import_module("modules.users_groups_auth").run()

    # 5 Ejecutar auditoría de Debian Tests
    print("[INFO] Ejecutando módulo: Debian Tests...\n")
    results["debian_tests"] = importlib.import_module("modules.debian_tests").run()

    # 6 Ejecutar auditoría de Debian Tests
    print("[INFO] Ejecutando módulo: Boot and services...\n")
    results["boot_services"] = importlib.import_module("modules.boot_services").run()

    # 7 Ejecutar auditoría de Network
    print("[INFO] Ejecutando módulo: Network...\n")
    results["network"] = importlib.import_module("modules.network").run()

    # 7 Ejecutar auditoría de File Permissions
    print("[INFO] Ejecutando módulo: File Permissions...\n")
    results["file_permissions"] = importlib.import_module("modules.file_permissions").run()

    # 7 Ejecutar auditoría de home directories
    print("[INFO] Ejecutando módulo: home directories...\n")
    results["home_directories"] = importlib.import_module("modules.home_directories").run()


    # 3️⃣ Aquí puedes agregar más módulos en el orden que quieras
    # print("[INFO] Ejecutando módulo: network...\n")
    # results["network"] = importlib.import_module("modules.network").run()

    return results

# Guardar el informe en JSON
def save_report(results):
    with open(REPORT_FILE, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[INFO] Auditoría finalizada. Revisa el reporte en {REPORT_FILE}\n")

# Ejecutar el programa
def main():
    check_root()
    setup_directories()
    
    # Ejecutar los módulos en el orden deseado
    results = run_selected_modules()
    
    # Guardar el reporte final
    save_report(results)

if __name__ == "__main__":
    main()
