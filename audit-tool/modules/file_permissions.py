import os
import stat
import json

def check_file_permissions(file_path):
    """Verifica los permisos de un archivo y devuelve su estado."""
    try:
        if os.path.exists(file_path):
            file_stat = os.stat(file_path)
            permissions = stat.filemode(file_stat.st_mode)
            # Recomendación si el archivo no tiene permisos adecuados
            if file_path in ["/boot/grub/grub.cfg", "/etc/crontab", "/etc/group", "/etc/passwd"]:
                return f"{permissions} [OK]"
            else:
                return f"{permissions} [SUGGESTION]"
        else:
            return f"{file_path} not found"
    except Exception as e:
        return f"Error al verificar permisos del archivo {file_path}: {str(e)}"

def check_directory_permissions(directory_path):
    """Verifica los permisos de un directorio y devuelve su estado."""
    try:
        if os.path.isdir(directory_path):
            dir_stat = os.stat(directory_path)
            permissions = stat.filemode(dir_stat.st_mode)
            # Recomendación si el directorio no tiene permisos adecuados
            if directory_path in ["/root/.ssh", "/etc/cron.d"]:
                return f"{permissions} [OK]"
            else:
                return f"{permissions} [SUGGESTION]"
        else:
            return f"{directory_path} not found"
    except Exception as e:
        return f"Error al verificar permisos del directorio {directory_path}: {str(e)}"

def run():
    """Ejecuta todas las comprobaciones de permisos de archivos y directorios."""
    print("[File Permissions] Iniciando comprobación de permisos de archivos y directorios...")

    # Lista de archivos importantes
    files_to_check = [
        "/boot/grub/grub.cfg", "/etc/crontab", "/etc/group", "/etc/hosts.allow", "/etc/hosts.deny",
        "/etc/issue", "/etc/issue.net", "/etc/passwd"
    ]
    
    # Lista de directorios importantes
    directories_to_check = [
        "/root/.ssh", "/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly", "/etc/cron.weekly", "/etc/cron.monthly"
    ]
    
    # Comprobación de archivos
    for file in files_to_check:
        result = check_file_permissions(file)
        print(f"File: {file} - {result}")
    
    # Comprobación de directorios
    for directory in directories_to_check:
        result = check_directory_permissions(directory)
        print(f"Directory: {directory} - {result}")

    print("---------------------------------------------------\n")

    return {
        "file_permissions": files_to_check,
        "directory_permissions": directories_to_check
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
