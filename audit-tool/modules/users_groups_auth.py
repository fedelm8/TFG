import subprocess
import os
import json

def check_admin_accounts():
    """Verifica las cuentas de administrador."""
    try:
        admins = subprocess.getoutput("getent group sudo")
        return "Found" if admins else "Not Found"
    except Exception as e:
        return f"Error al verificar cuentas de administrador: {str(e)}"

def check_unique_uids():
    """Verifica que los UIDs sean únicos."""
    try:
        uids = subprocess.getoutput("awk -F: '{print $3}' /etc/passwd")
        uid_list = uids.split('\n')
        unique_uids = len(uid_list) == len(set(uid_list))
        return "OK" if unique_uids else "Not Unique"
    except Exception as e:
        return f"Error al verificar UIDs únicos: {str(e)}"

def check_group_file_consistency():
    """Verifica la consistencia de los archivos de grupos."""
    try:
        group_check = subprocess.getoutput("grppck -r")
        return "OK" if "group file is consistent" in group_check else "Not Consistent"
    except Exception as e:
        return f"Error al verificar consistencia de archivos de grupos: {str(e)}"

def check_password_file_consistency():
    """Verifica la consistencia del archivo de contraseñas."""
    try:
        passwd_check = subprocess.getoutput("pwck -r")
        return "OK" if "passwd file is consistent" in passwd_check else "Not Consistent"
    except Exception as e:
        return f"Error al verificar consistencia del archivo de contraseñas: {str(e)}"

def check_password_hashing_methods():
    """Verifica los métodos de hashing de contraseñas."""
    try:
        shadow_file = subprocess.getoutput("cat /etc/shadow")
        if "$6$" in shadow_file:
            return "SHA-512"
        elif "$5$" in shadow_file:
            return "SHA-256"
        else:
            return "Other"
    except Exception as e:
        return f"Error al verificar el método de hashing de contraseñas: {str(e)}"

def check_password_hashing_rounds():
    """Verifica las rondas de hashing de contraseñas."""
    try:
        shadow_file = subprocess.getoutput("cat /etc/shadow")
        if "$6$" in shadow_file:
            return "Found"
        else:
            return "Not Found"
    except Exception as e:
        return f"Error al verificar rondas de hashing de contraseñas: {str(e)}"

def check_system_users():
    """Consulta los usuarios del sistema (no demonios)."""
    try:
        system_users = subprocess.getoutput("awk -F: '$3 >= 1000 {print $1}' /etc/passwd")
        return "Found" if system_users else "Not Found"
    except Exception as e:
        return f"Error al consultar usuarios del sistema: {str(e)}"

def check_nis_authentication_support():
    """Verifica el soporte para autenticación NIS."""
    try:
        nis_support = subprocess.getoutput("cat /etc/nsswitch.conf | grep nis")
        return "Enabled" if nis_support else "Not Enabled"
    except Exception as e:
        return f"Error al verificar soporte NIS: {str(e)}"

def check_sudoers_permissions():
    """Verifica los permisos del archivo sudoers y relacionados."""
    try:
        sudoers_permissions = subprocess.getoutput("ls -l /etc/sudoers")
        sudoers_d_permissions = subprocess.getoutput("ls -l /etc/sudoers.d")
        readme_permissions = subprocess.getoutput("ls -l /etc/sudoers.d/README")
        
        sudoers_result = "OK" if "root" in sudoers_permissions else "Warning"
        sudoers_d_result = "OK" if "root" in sudoers_d_permissions else "Warning"
        readme_result = "OK" if "root" in readme_permissions else "Warning"
        
        return {
            "sudoers_permissions": sudoers_result,
            "sudoers_d_permissions": sudoers_d_result,
            "readme_permissions": readme_result
        }
    except Exception as e:
        return f"Error al verificar los permisos de los archivos sudoers: {str(e)}"

def check_pam_configuration_files():
    """Verifica los archivos de configuración de PAM."""
    try:
        pam_conf = subprocess.getoutput("ls /etc/pam.d")
        return "Found" if pam_conf else "Not Found"
    except Exception as e:
        return f"Error al verificar archivos de configuración PAM: {str(e)}"

def check_locked_accounts():
    """Verifica las cuentas bloqueadas."""
    try:
        locked_accounts = subprocess.getoutput("passwd -S | grep 'L'")
        return "Found" if locked_accounts else "Not Found"
    except Exception as e:
        return f"Error al verificar cuentas bloqueadas: {str(e)}"

def check_expired_passwords():
    """Verifica contraseñas expiradas."""
    try:
        expired_passwords = subprocess.getoutput("chage -l $(whoami) | grep 'password expired'")
        return "Found" if expired_passwords else "Not Found"
    except Exception as e:
        return f"Error al verificar contraseñas expiradas: {str(e)}"

def check_user_password_aging():
    """Verifica el envejecimiento de las contraseñas de los usuarios."""
    try:
        password_aging = subprocess.getoutput("chage -l $(whoami)")
        return "OK" if "Last password change" in password_aging else "Not Found"
    except Exception as e:
        return f"Error al verificar envejecimiento de contraseñas: {str(e)}"

def check_single_user_mode_authentication():
    """Verifica la autenticación en el modo de usuario único de Linux."""
    try:
        single_user_mode = subprocess.getoutput("cat /etc/inittab | grep single")
        return "Found" if single_user_mode else "Not Found"
    except Exception as e:
        return f"Error al verificar autenticación en modo usuario único: {str(e)}"

def run():
    """Ejecuta todas las auditorías de usuarios, grupos y autenticación."""
    print("[Users, Groups and Authentication] Iniciando auditoría de usuarios, grupos y autenticación...")

    admin_accounts = check_admin_accounts()
    unique_uids = check_unique_uids()
    group_file_consistency = check_group_file_consistency()
    password_file_consistency = check_password_file_consistency()
    password_hashing_methods = check_password_hashing_methods()
    password_hashing_rounds = check_password_hashing_rounds()
    system_users = check_system_users()
    nis_auth_support = check_nis_authentication_support()
    sudoers_permissions = check_sudoers_permissions()
    pam_configuration_files = check_pam_configuration_files()
    locked_accounts = check_locked_accounts()
    expired_passwords = check_expired_passwords()
    user_password_aging = check_user_password_aging()
    single_user_mode_auth = check_single_user_mode_authentication()

    print("\n---------------------------------------------------")
    print(f"- Administrator accounts: {admin_accounts}")
    print(f"- Unique UIDs: {unique_uids}")
    print(f"- Consistency of group files (grppck): {group_file_consistency}")
    print(f"- Password file consistency: {password_file_consistency}")
    print(f"- Password hashing methods: {password_hashing_methods}")
    print(f"- Checking password hashing rounds: {password_hashing_rounds}")
    print(f"- Query system users (non daemons): {system_users}")
    print(f"- NIS+ authentication support: {nis_auth_support}")
    print(f"- Sudoers file(s): Found")
    print(f"  - Permissions for directory: /etc/sudoers.d: {sudoers_permissions['sudoers_d_permissions']}")
    print(f"  - Permissions for: /etc/sudoers: {sudoers_permissions['sudoers_permissions']}")
    print(f"  - Permissions for: /etc/sudoers.d/README: {sudoers_permissions['readme_permissions']}")
    print(f"- PAM configuration files: {pam_configuration_files}")
    print(f"- Locked accounts: {locked_accounts}")
    print(f"- Checking expired passwords: {expired_passwords}")
    print(f"- Checking user password aging (minimum): {user_password_aging}")
    print(f"- Checking Linux single user mode authentication: {single_user_mode_auth}")
    print("---------------------------------------------------\n")

    return {
        "admin_accounts": admin_accounts,
        "unique_uids": unique_uids,
        "group_file_consistency": group_file_consistency,
        "password_file_consistency": password_file_consistency,
        "password_hashing_methods": password_hashing_methods,
        "password_hashing_rounds": password_hashing_rounds,
        "system_users": system_users,
        "nis_auth_support": nis_auth_support,
        "sudoers_permissions": sudoers_permissions,
        "pam_configuration_files": pam_configuration_files,
        "locked_accounts": locked_accounts,
        "expired_passwords": expired_passwords,
        "user_password_aging": user_password_aging,
        "single_user_mode_auth": single_user_mode_auth
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
