import os
import platform
import subprocess
import psutil
import json
import locale

def get_system_info():
    """Obtiene información detallada del sistema."""
    try:
        system_language, _ = locale.getdefaultlocale()
        info = {
            "program_version": "1.0.0",  # Versión de la herramienta
            "operating_system": platform.system(),
            "operating_system_name": platform.platform(),
            "operating_system_version": platform.version(),
            "kernel_version": platform.release(),
            "hardware_platform": platform.machine(),
            "hostname": platform.node(),
            "uptime": subprocess.getoutput("uptime -p"),
            "cpu_count": psutil.cpu_count(logical=True),
            "total_memory": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "available_memory": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            "disk_usage": f"{psutil.disk_usage('/').percent}%",
            "user_running_script": os.getlogin(),
            "language": system_language if system_language else "Unknown"
        }
        return info
    except Exception as e:
        return {"error": str(e)}

def run():
    """Ejecuta la auditoría de información del sistema y devuelve los resultados."""
    print("[System Info] Recopilando información del sistema...")
    system_data = get_system_info()
    
    print("\n---------------------------------------------------")
    for key, value in system_data.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("---------------------------------------------------\n")
    
    return system_data

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
