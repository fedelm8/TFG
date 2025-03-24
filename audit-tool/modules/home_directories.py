import os
import stat
import pwd
import json

def check_home_directory_permissions():
    """Verifica los permisos de los directorios de inicio de los usuarios."""
    try:
        home_dirs = [f"/home/{user}" for user in os.listdir('/home') if os.path.isdir(f"/home/{user}")]
        permissions = {}
        
        for home in home_dirs:
            home_stat = os.stat(home)
            perm = stat.filemode(home_stat.st_mode)
            if perm == "-rwx------":  # Verifica que los permisos sean correctos (700)
                permissions[home] = f"{perm} [OK]"
            else:
                permissions[home] = f"{perm} [SUGGESTION]"
        
        return permissions
    except Exception as e:
        return f"Error al verificar permisos de directorios de inicio: {str(e)}"

def check_home_directory_ownership():
    """Verifica que el propietario de los directorios de inicio sea el usuario correcto."""
    try:
        home_dirs = [f"/home/{user}" for user in os.listdir('/home') if os.path.isdir(f"/home/{user}")]
        ownership = {}
        
        for home in home_dirs:
            stat_info = os.stat(home)
            user_name = pwd.getpwuid(stat_info.st_uid).pw_name
            if user_name == os.path.basename(home):  # El propietario debe coincidir con el nombre del directorio
                ownership[home] = f"Owner: {user_name} [OK]"
            else:
                ownership[home] = f"Owner: {user_name} [SUGGESTION]"
        
        return ownership
    except Exception as e:
        return f"Error al verificar propiedad de directorios de inicio: {str(e)}"

def check_shell_history_files():
    """Verifica la existencia y permisos de los archivos de historial de shell."""
    try:
        home_dirs = [f"/home/{user}" for user in os.listdir('/home') if os.path.isdir(f"/home/{user}")]
        history_files = {}
        
        for home in home_dirs:
            bash_history = os.path.join(home, ".bash_history")
            zsh_history = os.path.join(home, ".zsh_history")
            history_permissions = "OK"
            
            # Comprobar si los archivos existen y sus permisos
            if os.path.exists(bash_history):
                bash_stat = os.stat(bash_history)
                bash_perm = stat.filemode(bash_stat.st_mode)
                if bash_perm != "-rw-------":  # Permisos 600 recomendados
                    history_permissions = "SUGGESTION"
                history_files[bash_history] = f"{bash_perm} [OK]" if history_permissions == "OK" else f"{bash_perm} [SUGGESTION]"
            
            if os.path.exists(zsh_history):
                zsh_stat = os.stat(zsh_history)
                zsh_perm = stat.filemode(zsh_stat.st_mode)
                if zsh_perm != "-rw-------":  # Permisos 600 recomendados
                    history_permissions = "SUGGESTION"
                history_files[zsh_history] = f"{zsh_perm} [OK]" if history_permissions == "OK" else f"{zsh_perm} [SUGGESTION]"

        return history_files
    except Exception as e:
        return f"Error al verificar archivos de historial de shell: {str(e)}"

def run():
    """Ejecuta todas las auditorías de directorios de inicio y devuelve los resultados."""
    print("[Home Directories] Iniciando auditoría de directorios de inicio...")

    home_permissions = check_home_directory_permissions()
    home_ownership = check_home_directory_ownership()
    history_files = check_shell_history_files()

    print("\n---------------------------------------------------")
    print("[Permissions of Home Directories]")
    for directory, permission in home_permissions.items():
        print(f"  - {directory}: {permission}")
    
    print("[Ownership of Home Directories]")
    for directory, owner in home_ownership.items():
        print(f"  - {directory}: {owner}")
    
    print("[Checking Shell History Files]")
    for file, permission in history_files.items():
        print(f"  - {file}: {permission}")
    
    print("---------------------------------------------------\n")

    return {
        "home_permissions": home_permissions,
        "home_ownership": home_ownership,
        "history_files": history_files
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
