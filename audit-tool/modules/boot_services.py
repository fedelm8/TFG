import subprocess
import os
import json


def check_service_manager():
    """Verifica qué gestor de servicios está en uso."""
    try:
        service_manager = subprocess.getoutput("ps -p 1 -o comm=")
        return service_manager if service_manager else "Not Found"
    except Exception as e:
        return f"Error al verificar el gestor de servicios: {str(e)}"

def check_uefi_boot():
    """Verifica si el sistema está utilizando UEFI."""
    try:
        uefi_boot = subprocess.getoutput("ls /sys/firmware/efi")
        return "Found" if uefi_boot else "Not Found"
    except Exception as e:
        return f"Error al verificar UEFI boot: {str(e)}"

def check_grub2_presence():
    """Verifica si GRUB2 está presente en el sistema."""
    try:
        grub_check = subprocess.getoutput("ls /boot/grub")
        return "Found" if grub_check else "Not Found"
    except Exception as e:
        return f"Error al verificar GRUB2: {str(e)}"

def check_password_protection():
    """Verifica si el sistema tiene protección por contraseña configurada."""
    try:
        password_protection = subprocess.getoutput("grep -i password /etc/grub.d/40_custom")
        return "Found" if password_protection else "Not Found"
    except Exception as e:
        return f"Error al verificar protección por contraseña: {str(e)}"

def check_running_services():
    """Verifica los servicios en ejecución."""
    try:
        running_services = subprocess.getoutput("systemctl list-units --type=service --state=running")
        return len(running_services.split('\n')) - 1  # Restar la línea de encabezado
    except Exception as e:
        return f"Error al verificar servicios en ejecución: {str(e)}"

def check_enabled_services_at_boot():
    """Verifica los servicios habilitados para arrancar al inicio."""
    try:
        enabled_services = subprocess.getoutput("systemctl list-unit-files --type=service --state=enabled")
        return len(enabled_services.split('\n')) - 1  # Restar la línea de encabezado
    except Exception as e:
        return f"Error al verificar servicios habilitados: {str(e)}"

def check_startup_files_permissions():
    """Verifica los permisos de los archivos de inicio."""
    try:
        permissions = subprocess.getoutput("ls -l /etc/init.d")
        return "OK" if permissions else "Not Found"
    except Exception as e:
        return f"Error al verificar permisos de archivos de inicio: {str(e)}"

def run_systemd_analyze_security():
    """Ejecuta systemd-analyze security para verificar la seguridad de los servicios."""
    try:
        security_analysis = subprocess.getoutput("systemd-analyze security")
        return security_analysis
    except Exception as e:
        return f"Error al ejecutar systemd-analyze security: {str(e)}"

def run():
    """Ejecuta todas las auditorías de arranque y servicios y devuelve los resultados."""
    print("[Boot and Services] Iniciando auditoría de arranque y servicios...")

    service_manager = check_service_manager()
    uefi_boot = check_uefi_boot()
    grub2_presence = check_grub2_presence()
    password_protection = check_password_protection()
    running_services = check_running_services()
    enabled_services = check_enabled_services_at_boot()
    startup_files_permissions = check_startup_files_permissions()
    security_analysis = run_systemd_analyze_security()

    print("\n---------------------------------------------------")
    print(f"- Service Manager: {service_manager}")
    print(f"- UEFI Boot: {uefi_boot}")
    print(f"- GRUB2 Presence: {grub2_presence}")
    print(f"- Password Protection: {password_protection}")
    print(f"- Running services: {running_services} services running")
    print(f"- Enabled services at boot: {enabled_services} services enabled")
    print(f"- Startup files (permissions): {startup_files_permissions}")
    print("- Running 'systemd-analyze security':")
    print(security_analysis)
    print("---------------------------------------------------\n")

    return {
        "service_manager": service_manager,
        "uefi_boot": uefi_boot,
        "grub2_presence": grub2_presence,
        "password_protection": password_protection,
        "running_services": running_services,
        "enabled_services": enabled_services,
        "startup_files_permissions": startup_files_permissions,
        "security_analysis": security_analysis
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
