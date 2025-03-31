import smtplib
from email.mime.text import MIMEText
import os
import signal

LOG_FILE = "/ruta/a/mi_herramienta/logs/alertas.log"  # Ruta completa al archivo de logs

# Asegurarse de que el archivo de logs exista
def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w'):  # Crear el archivo vacío si no existe
            pass

def log_alert(message):
    ensure_log_file()
    with open(LOG_FILE, 'a') as log:
        log.write(message + "\n")

def send_alert(message):
    subject = "Alerta: Acción no permitida detectada"
    body = f"Se ha detectado una acción no permitida: {message}"
    try:
        with smtplib.SMTP('smtp.example.com') as server:
            server.login('tu_correo@example.com', 'tu_contraseña')
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = 'tu_correo@example.com'
            msg['To'] = 'destinatario@example.com'
            server.sendmail('tu_correo@example.com', 'destinatario@example.com', msg.as_string())
            print("Alerta enviada por correo.")
        
        # Registrar la alerta en el archivo de logs
        log_alert(f"Alerta enviada: {message}")
        
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def block_action(message):
    print(f"Bloqueando acción: {message}")
    pid = extract_pid_from_message(message)  # Función para extraer el PID del mensaje
    try:
        os.kill(pid, signal.SIGKILL)
        print(f"Proceso con PID {pid} ha sido detenido.")
    except Exception as e:
        print(f"Error al bloquear el proceso: {e}")

def extract_pid_from_message(message):
    return 1234  # Este es un valor simulado, se debe extraer dinámicamente
