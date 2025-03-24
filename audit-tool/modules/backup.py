import subprocess
import os
import json


def check_backup_schedule():
    """Verifica si las copias de seguridad se realizan regularmente."""
    try:
        # Verificar si hay trabajos programados de copias de seguridad (por ejemplo, con cron)
        cron_jobs = subprocess.getoutput("crontab -l")
        if cron_jobs:
            backup_jobs = [job for job in cron_jobs.splitlines() if 'backup' in job]
            if backup_jobs:
                return f"Backup jobs found:\n{chr(10).join(backup_jobs)}"
            else:
                return "No backup jobs scheduled in cron.\nEnsure backups are scheduled regularly."
        else:
            return "No cron jobs found.\nEnsure that backup jobs are scheduled using cron or another task scheduler."
    except Exception as e:
        return f"Error checking backup schedule: {str(e)}"

def check_backup_storage():
    """Verifica si las copias de seguridad están almacenadas de forma segura."""
    try:
        # Reemplaza con la ruta de tu directorio de backups
        backup_dir = "/backup"  
        if os.path.exists(backup_dir) and os.access(backup_dir, os.R_OK):
            return f"Backup directory found: {backup_dir}\nEnsure the backup directory is secure and properly configured."
        else:
            return f"Backup directory not found or not accessible at {backup_dir}.\nEnsure that the backup directory exists and is properly secured."
    except Exception as e:
        return f"Error checking backup storage: {str(e)}"

def check_backup_encryption():
    """Verifica si las copias de seguridad están cifradas."""
    try:
        # Cambia la ruta según la ubicación de tus copias de seguridad cifradas
        backup_dir = "/backup"  
        # Verificar si las copias de seguridad cifradas están en el directorio (con extensión .gpg)
        if os.path.exists(backup_dir):
            encrypted_backups = subprocess.getoutput(f"ls {backup_dir} | grep '.gpg'")
            if encrypted_backups:
                return f"Encrypted backups found: {encrypted_backups}"
            else:
                return "No encrypted backups found.\nConsider encrypting your backups if they contain sensitive data."
        else:
            return f"Backup directory not found or not accessible at {backup_dir}."
    except Exception as e:
        return f"Error checking backup encryption: {str(e)}"

def check_restore_process():
    """Verifica si el proceso de restauración de las copias de seguridad está configurado y es válido."""
    try:
        # Comprobar si el proceso de restauración está documentado o configurado (por ejemplo, un script de restauración)
        restore_script = "/usr/local/bin/restore_backup.sh"  # Ruta de un script de restauración
        if os.path.exists(restore_script) and os.access(restore_script, os.X_OK):
            return f"Backup restore script found: {restore_script}\nEnsure that the restore process is tested and documented."
        else:
            return "No backup restore script found.\nEnsure that a restore process is documented and tested for disaster recovery."
    except Exception as e:
        return f"Error checking backup restore process: {str(e)}"

def run():
    """Ejecuta todas las auditorías de copias de seguridad y devuelve los resultados."""
    print("[Backup] Starting backup audit...")

    backup_schedule = check_backup_schedule()
    backup_storage = check_backup_storage()
    backup_encryption = check_backup_encryption()
    restore_process = check_restore_process()

    print("\n---------------------------------------------------")
    print(f"- Backup schedule: {backup_schedule}")
    print(f"- Backup storage: {backup_storage}")
    print(f"- Backup encryption: {backup_encryption}")
    print(f"- Restore process: {restore_process}")
    print("---------------------------------------------------\n")

    return {
        "backup_schedule": backup_schedule,
        "backup_storage": backup_storage,
        "backup_encryption": backup_encryption,
        "restore_process": restore_process
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
