import subprocess
import os

def check_pending_updates():
    """Verifica si hay actualizaciones críticas pendientes."""
    try:
        # Ejecutar el comando de actualización de la lista de paquetes
        updates = subprocess.getoutput("apt list --upgradable")
        if "upgradable from" in updates:
            return f"Pending updates found: {updates}"
        else:
            return "No pending updates found."
    except Exception as e:
        return f"Error al verificar actualizaciones pendientes: {str(e)}"

def check_repository_configuration():
    """Verifica si los repositorios están configurados de manera segura."""
    try:
        # Verificar los repositorios en /etc/apt/sources.list y /etc/apt/sources.list.d/
        sources_files = ["/etc/apt/sources.list"] + [f"/etc/apt/sources.list.d/{file}" for file in os.listdir("/etc/apt/sources.list.d")]

        insecure_repos = []
        for file in sources_files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if 'http://' in line:  # Repositorios no cifrados
                            insecure_repos.append(file)

        if insecure_repos:
            return f"Insecure repositories found: {', '.join(insecure_repos)}"
        else:
            return "All repositories are secure (using https)."
    except Exception as e:
        return f"Error al verificar la configuración de repositorios: {str(e)}"

def check_automatic_updates():
    """Verifica si las actualizaciones automáticas están configuradas adecuadamente."""
    try:
        # Verificar si los paquetes de actualizaciones automáticas están instalados
        package_check = subprocess.getoutput("dpkg -l | grep unattended-upgrades")
        if package_check:
            # Verificar que la configuración de actualizaciones automáticas esté habilitada
            config_check = subprocess.getoutput("cat /etc/apt/apt.conf.d/20auto-upgrades")
            if "APT::Periodic::Update-Package-Lists" in config_check and "1" in config_check:
                return "Automatic updates are configured correctly."
            else:
                return "Automatic updates are not configured correctly."
        else:
            return "Unattended-upgrades package is not installed."
    except Exception as e:
        return f"Error al verificar actualizaciones automáticas: {str(e)}"

def run():
    """Ejecuta todas las auditorías de actualizaciones del sistema y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[System Updates] Iniciando auditoría de actualizaciones del sistema...")

    pending_updates = check_pending_updates()
    repository_configuration = check_repository_configuration()
    automatic_updates = check_automatic_updates()

    print("\n---------------------------------------------------")
    print(f"- Pending updates: {pending_updates}")
    print(f"- Repository configuration: {repository_configuration}")
    print(f"- Automatic updates: {automatic_updates}")
    print("---------------------------------------------------\n")

    return {
        "pending_updates": pending_updates,
        "repository_configuration": repository_configuration,
        "automatic_updates": automatic_updates
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
