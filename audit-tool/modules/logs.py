import os
import subprocess
import time

def check_log_file_exists(log_file):
    """Verifica si un archivo de log existe."""
    try:
        if os.path.exists(log_file):
            return f"{log_file}: [FOUND]"
        else:
            return f"{log_file}: [NOT FOUND]"
    except Exception as e:
        return f"Error al verificar existencia de {log_file}: {str(e)}"

def check_log_integrity(log_file):
    """Verifica la integridad de un archivo de log (no debe estar vacío)."""
    try:
        if os.path.exists(log_file):
            if os.path.getsize(log_file) > 0:
                return f"{log_file}: [OK]"
            else:
                return f"{log_file}: [EMPTY]"
        else:
            return f"{log_file}: [NOT FOUND]"
    except Exception as e:
        return f"Error al verificar integridad de {log_file}: {str(e)}"

def check_log_rotation():
    """Verifica la configuración de rotación de logs en /etc/logrotate.d/."""
    try:
        logrotate_conf = "/etc/logrotate.d/"
        files = os.listdir(logrotate_conf)
        if files:
            return f"Log rotation configuration: [FOUND] in {logrotate_conf}"
        else:
            return f"Log rotation configuration: [NOT FOUND]"
    except Exception as e:
        return f"Error al verificar la configuración de rotación de logs: {str(e)}"

def check_old_logs(log_file, days_threshold=30):
    """Verifica si los logs son antiguos (más de 30 días por defecto)."""
    try:
        if os.path.exists(log_file):
            file_mod_time = os.path.getmtime(log_file)
            days_old = (time.time() - file_mod_time) / (60 * 60 * 24)
            if days_old > days_threshold:
                return f"{log_file}: [OLD] ({days_old:.2f} days)"
            else:
                return f"{log_file}: [OK] ({days_old:.2f} days)"
        else:
            return f"{log_file}: [NOT FOUND]"
    except Exception as e:
        return f"Error al verificar la antigüedad de {log_file}: {str(e)}"

def run():
    """Ejecuta todas las auditorías de los logs y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Logs] Iniciando auditoría de logs...")

    log_files = ["/var/log/auth.log", "/var/log/syslog", "/var/log/messages", "/var/log/dmesg"]
    
    # Verificación de existencia y estado de los archivos de log
    for log_file in log_files:
        print(check_log_file_exists(log_file))
        print(check_log_integrity(log_file))
        print(check_old_logs(log_file))
    
    # Verificación de la configuración de rotación de logs
    print(check_log_rotation())
    
    print("---------------------------------------------------\n")

    return {
        "log_files": log_files,
        "log_rotation_status": check_log_rotation(),
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
