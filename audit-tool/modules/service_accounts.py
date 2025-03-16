import subprocess
import pwd
import crypt
import time

def check_service_accounts_with_elevated_privileges():
    """Verifica si hay cuentas de servicio con privilegios elevados (sudo/root)."""
    try:
        # Buscar cuentas con privilegios de sudo
        sudo_accounts = subprocess.getoutput("grep -E 'sudo|root' /etc/group")
        if sudo_accounts:
            return "Service accounts with elevated privileges found."
        else:
            return "No service accounts with elevated privileges found."
    except Exception as e:
        return f"Error al verificar cuentas de servicio con privilegios elevados: {str(e)}"

def check_encrypted_passwords_for_service_accounts():
    """Verifica que las contraseñas de las cuentas de servicio estén cifradas correctamente."""
    try:
        # Verifica que las contraseñas en /etc/shadow estén cifradas (no en texto claro)
        shadow_file = subprocess.getoutput("cat /etc/shadow")
        if shadow_file:
            accounts = shadow_file.splitlines()
            unencrypted_accounts = []
            for account in accounts:
                username = account.split(":")[0]
                password = account.split(":")[1]
                if password == "":  # Contraseña vacía (sin cifrar)
                    unencrypted_accounts.append(username)

            if unencrypted_accounts:
                return f"Unencrypted passwords found for accounts: {', '.join(unencrypted_accounts)}"
            else:
                return "All service accounts have encrypted passwords."
        else:
            return "Error reading /etc/shadow."
    except Exception as e:
        return f"Error al verificar contraseñas cifradas de cuentas de servicio: {str(e)}"

def check_inactive_service_accounts():
    """Verifica si hay cuentas de servicio inactivas o no utilizadas."""
    try:
        inactive_accounts = []
        accounts = subprocess.getoutput("cat /etc/passwd").splitlines()
        for account in accounts:
            username = account.split(":")[0]
            lastlog_output = subprocess.getoutput(f"lastlog -u {username}")
            lastlog_lines = lastlog_output.splitlines()

            # Si lastlog no tiene un registro para el usuario (como 'Never logged in')
            if len(lastlog_lines) < 2:
                continue  # Si no hay información, continuamos con la siguiente cuenta

            last_log_time = lastlog_lines[-1].split()[3]

            # Verificar si la fecha está en el formato esperado (y evitar el error)
            try:
                last_log_timestamp = time.mktime(time.strptime(last_log_time, "%b %d"))
            except ValueError:
                continue  # Si no se puede convertir, continuamos con la siguiente cuenta

            current_time = time.time()

            # Si la cuenta no ha iniciado sesión en los últimos 30 días, se considera inactiva
            if (current_time - last_log_timestamp) > (30 * 24 * 60 * 60):
                inactive_accounts.append(username)

        if inactive_accounts:
            return f"Inactive service accounts found: {', '.join(inactive_accounts)}"
        else:
            return "No inactive service accounts found."
    except Exception as e:
        return f"Error al verificar cuentas de servicio inactivas: {str(e)}"

def run():
    """Ejecuta todas las auditorías de las cuentas de servicio y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Service Accounts] Iniciando auditoría de cuentas de servicio...")

    elevated_privileges = check_service_accounts_with_elevated_privileges()
    encrypted_passwords = check_encrypted_passwords_for_service_accounts()
    inactive_accounts = check_inactive_service_accounts()

    print("\n---------------------------------------------------")
    print(f"- Service accounts with elevated privileges: {elevated_privileges}")
    print(f"- Encrypted passwords for service accounts: {encrypted_passwords}")
    print(f"- Inactive service accounts: {inactive_accounts}")
    print("---------------------------------------------------\n")

    return {
        "elevated_privileges": elevated_privileges,
        "encrypted_passwords": encrypted_passwords,
        "inactive_accounts": inactive_accounts
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
