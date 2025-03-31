import subprocess
import time
from alerta import send_alert, block_action

def monitor_audit_logs():
    # Comando para leer los registros de auditd en tiempo real
    command = "ausearch -k shadow-access -k passwd-access -m execve"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    while True:
        line = process.stdout.readline().decode('utf-8')
        if line:
            print(f"Evento detectado: {line.strip()}")
            # Detectar si hay acceso a /etc/shadow
            if "/etc/shadow" in line:
                send_alert("Acceso detectado a /etc/shadow")
                block_action(line)
            
            # Detectar si hay acceso a /etc/passwd
            elif "/etc/passwd" in line:
                send_alert("Acceso detectado a /etc/passwd")
                block_action(line)

if __name__ == "__main__":
    print("Monitor de accesos a archivos sensibles iniciado...")
    monitor_audit_logs()
