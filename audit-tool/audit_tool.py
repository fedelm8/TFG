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

    # 8 Ejecutar auditoría de File Permissions
    print("[INFO] Ejecutando módulo: File Permissions...\n")
    results["file_permissions"] = importlib.import_module("modules.file_permissions").run()

    # 9 Ejecutar auditoría de home directories
    print("[INFO] Ejecutando módulo: home directories...\n")
    results["home_directories"] = importlib.import_module("modules.home_directories").run()

    # 10 Ejecutar auditoría de logs
    print("[INFO] Ejecutando módulo: Auditing Logs...\n")
    results["logs"] = importlib.import_module("modules.logs").run()

    # 11 Ejecutar auditoría de seguridad de aplicaciones
    print("[INFO] Ejecutando módulo: Auditing Security App...\n")
    results["app_security"] = importlib.import_module("modules.app_security").run()

    # 12 Ejecutar auditoría avanzada de red
    print("[INFO] Ejecutando módulo: Advanced Network Auditing ...\n")
    results["advanced_network_security"] = importlib.import_module("modules.advanced_network_security").run()

    # 13 Ejecutar auditoría de cuentas de servicio
    print("[INFO] Ejecutando módulo: Account Service Auditing ...\n")
    results["service_accounts"] = importlib.import_module("modules.service_accounts").run()

    # 14 Ejecutar auditoría de seguridad de Contenedores
    print("[INFO] Ejecutando módulo: Containers Security Auditing ...\n")
    results["containers_security"] = importlib.import_module("modules.containers_security").run()

    # 15 Ejecutar auditoría de actualizaciones
    print("[INFO] Ejecutando módulo: Updates Auditing ...\n")
    results["updates"] = importlib.import_module("modules.updates").run()

    # 16 Ejecutar auditoría de politicas de seguridad
    print("[INFO] Ejecutando módulo: Security Policies Auditing ...\n")
    results["security_policies"] = importlib.import_module("modules.security_policies").run()

    # 17 Ejecutar auditoría de privilegios elevados
    print("[INFO] Ejecutando módulo: Sudo Auditing ...\n")
    results["sudo"] = importlib.import_module("modules.sudo").run()

    # 18 Ejecutar auditoría de seguridad de dispositivos de almacenamiento
    print("[INFO] Ejecutando módulo: Storage Device Auditing ...\n")
    results["storage_device"] = importlib.import_module("modules.storage_device").run()

    # 19 Ejecutar auditoría de proteccion de malware
    print("[INFO] Ejecutando módulo: Malware Protection Auditing ...\n")
    results["malware_protection"] = importlib.import_module("modules.malware_protection").run()

    # 20 Ejecutar auditoría de copias de seguridad
    print("[INFO] Ejecutando módulo: Backup Auditing ...\n")
    results["backup"] = importlib.import_module("modules.backup").run()


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
