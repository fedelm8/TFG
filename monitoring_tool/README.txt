# Herramienta de Monitoreo de Accesos a Archivos Sensibles

## Descripción

Esta herramienta monitorea en tiempo real los accesos a archivos sensibles del sistema, como `/etc/shadow` y `/etc/passwd`, que son comúnmente utilizados para la gestión de contraseñas y usuarios en sistemas Linux. 

Cuando la herramienta detecta un intento de acceso no autorizado a estos archivos, realiza las siguientes acciones:
- Envía una alerta por correo electrónico.
- Bloquea el proceso relacionado con el acceso, si es necesario.

La herramienta se ejecuta como un servicio en segundo plano mediante **`systemd`**, lo que permite que se ejecute de manera continua incluso después de reiniciar el sistema.

---

## **Requisitos**

### **Dependencias del sistema**
1. **`auditd`**: Necesario para auditar los accesos a archivos sensibles.
   - Instalación:
     ```bash
     sudo apt-get install auditd
     ```

2. **Python 3.x**: Necesario para ejecutar los scripts.
   - Asegúrate de tener Python 3 instalado.
   - Puedes verificar la versión de Python con:
     ```bash
     python3 --version
     ```

3. **Bibliotecas de Python** (si las necesitas):
   Si la herramienta requiere bibliotecas adicionales, instala las dependencias con:
   ```bash
   pip install -r requirements.txt
