import subprocess
import json

def check_meminfo():
    """Verifica el archivo /proc/meminfo."""
    try:
        meminfo = subprocess.getoutput("cat /proc/meminfo")
        return "Found" if meminfo else "Not Found"
    except Exception as e:
        return f"Error al verificar /proc/meminfo: {str(e)}"

def check_dead_zombie_processes():
    """Busca procesos muertos/zombie."""
    try:
        zombie_processes = subprocess.getoutput("ps aux | grep 'Z'")
        return "Found" if zombie_processes else "Not Found"
    except Exception as e:
        return f"Error al buscar procesos zombie: {str(e)}"

def check_io_waiting_processes():
    """Busca procesos en espera de I/O."""
    try:
        io_waiting = subprocess.getoutput("ps aux | awk '$8 == \"D\"'")
        return "Found" if io_waiting else "Not Found"
    except Exception as e:
        return f"Error al buscar procesos en espera de I/O: {str(e)}"

def check_prelink_tooling():
    """Busca si la herramienta prelink está instalada."""
    try:
        prelink = subprocess.getoutput("which prelink")
        return "Found" if prelink else "Not Found"
    except Exception as e:
        return f"Error al verificar la herramienta prelink: {str(e)}"

def run():
    """Ejecuta todas las auditorías de memoria y procesos y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Memory and Processes] Iniciando auditoría de memoria y procesos...")

    meminfo = check_meminfo()
    zombie_processes = check_dead_zombie_processes()
    io_waiting_processes = check_io_waiting_processes()
    prelink_tooling = check_prelink_tooling()

    print("\n---------------------------------------------------")
    print(f"- Checking /proc/meminfo: {meminfo}")
    print(f"- Searching for dead/zombie processes: {zombie_processes}")
    print(f"- Searching for IO waiting processes: {io_waiting_processes}")
    print(f"- Search prelink tooling: {prelink_tooling}")
    print("---------------------------------------------------\n")

    return {
        "meminfo": meminfo,
        "zombie_processes": zombie_processes,
        "io_waiting_processes": io_waiting_processes,
        "prelink_tooling": prelink_tooling
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
