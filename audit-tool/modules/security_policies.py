import subprocess
import json

def check_password_policy():
    """Verifica las políticas de contraseñas configuradas en el sistema."""
    try:
        # Verificar políticas de contraseñas en /etc/login.defs
        login_defs = subprocess.getoutput("cat /etc/login.defs")
        password_policy = {}

        # Longitud mínima de la contraseña
        min_length = subprocess.getoutput("grep -i 'PASS_MIN_LEN' /etc/login.defs")
        password_policy["Min Length"] = min_length.split()[-1] if min_length and not min_length.startswith("#") else "Not Set or Commented"

        # Edad mínima de la contraseña
        min_age = subprocess.getoutput("grep -i 'PASS_MIN_DAYS' /etc/login.defs")
        password_policy["Min Age"] = min_age.split()[-1] if min_age and not min_age.startswith("#") else "Not Set or Commented"

        # Edad máxima de la contraseña
        max_age = subprocess.getoutput("grep -i 'PASS_MAX_DAYS' /etc/login.defs")
        password_policy["Max Age"] = max_age.split()[-1] if max_age and not max_age.startswith("#") else "Not Set or Commented"

        # Advertencia antes de expiración de la contraseña
        warn_age = subprocess.getoutput("grep -i 'PASS_WARN_AGE' /etc/login.defs")
        password_policy["Warn Age"] = warn_age.split()[-1] if warn_age and not warn_age.startswith("#") else "Not Set or Commented"

        return password_policy
    except Exception as e:
        return f"Error al verificar políticas de contraseñas: {str(e)}"

def check_audit_logs():
    """Verifica que los logs de auditoría estén habilitados para acciones de usuario y sistema."""
    try:
        # Verificar configuración de auditoría en /etc/audit/auditd.conf
        audit_config = subprocess.getoutput("cat /etc/audit/auditd.conf")

        # Verificar que la auditoría esté activada
        audit_status = "Auditd configured correctly" if "active = yes" in audit_config else "Auditd not properly configured"

        # Verificar que la auditoría se registre en un archivo
        log_file_check = subprocess.getoutput("grep -i 'log_file' /etc/audit/auditd.conf")
        audit_status += ", Log file configured correctly" if "log_file" in log_file_check else ", Log file not configured properly"

        return audit_status
    except Exception as e:
        return f"Error al verificar configuración de logs de auditoría: {str(e)}"

def run():
    """Ejecuta todas las auditorías de políticas de seguridad y devuelve los resultados."""
    print("[Security Policies] Iniciando auditoría de políticas de seguridad...")

    password_policy = check_password_policy()
    audit_logs = check_audit_logs()

    print("\n---------------------------------------------------")
    print("[Password Policies]")
    for policy, value in password_policy.items():
        print(f"  - {policy}: {value}")

    print(f"- Audit Logs: {audit_logs}")
    print("---------------------------------------------------\n")

    return {
        "password_policy": password_policy,
        "audit_logs": audit_logs
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
