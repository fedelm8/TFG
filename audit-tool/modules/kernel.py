import subprocess
import json

def get_kernel_version():
    """Obtiene la versión del kernel del sistema."""
    try:
        return subprocess.getoutput("uname -r")
    except Exception as e:
        return f"Error al obtener la versión del kernel: {str(e)}"

def check_aslr():
    """Verifica si ASLR (Address Space Layout Randomization) está habilitado."""
    try:
        with open("/proc/sys/kernel/randomize_va_space") as f:
            aslr_value = f.read().strip()
        return "Habilitado" if aslr_value == "2" else "Deshabilitado"
    except Exception as e:
        return f"Error al verificar ASLR: {str(e)}"

def check_kernel_parameters():
    """Verifica parámetros de seguridad en sysctl relacionados con el kernel."""
    params = {
        "kernel.kptr_restrict": "Restricción de acceso a direcciones de memoria del kernel",
        "kernel.dmesg_restrict": "Restricción de acceso a logs del kernel",
        "kernel.yama.ptrace_scope": "Protección contra ptrace (depuración de procesos)"
    }
    results = {}
    for param, desc in params.items():
        try:
            value = subprocess.getoutput(f"sysctl -n {param}")
            results[param] = {"value": value, "description": desc}
        except Exception as e:
            results[param] = {"error": str(e)}
    return results

def check_kernel_modules():
    """Lista módulos del kernel cargados y revisa si hay módulos peligrosos activos."""
    try:
        modules = subprocess.getoutput("lsmod").split('\n')[1:]
        dangerous_modules = ["usb_storage", "firewire_core", "nfs", "cramfs", "jffs2"]
        loaded_modules = []
        flagged_modules = []
        
        for mod in modules:
            mod_name = mod.split()[0]
            loaded_modules.append(mod_name)
            if mod_name in dangerous_modules:
                flagged_modules.append(mod_name)
        
        return {
            "loaded_modules": loaded_modules[:10],  # Limitar a 10 módulos para mejor visualización
            "flagged_modules": flagged_modules if flagged_modules else "Ningún módulo sospechoso cargado"
        }
    except Exception as e:
        return {"error": str(e)}

def check_kernel_hardening():
    """Verifica configuraciones avanzadas de seguridad del kernel."""
    checks = {
        "kernel.unprivileged_bpf_disabled": "Deshabilitar BPF para usuarios no root",
        "kernel.kexec_load_disabled": "Evitar la carga arbitraria de imágenes del kernel",
        "vm.mmap_min_addr": "Protección contra mmap en direcciones bajas"
    }
    results = {}
    for param, desc in checks.items():
        try:
            value = subprocess.getoutput(f"sysctl -n {param}")
            results[param] = {"value": value, "description": desc}
        except Exception as e:
            results[param] = {"error": str(e)}
    return results

# Nuevas funciones añadidas

def check_runlevel():
    """Verifica el nivel de ejecución predeterminado."""
    try:
        runlevel = subprocess.getoutput("runlevel")
        return f"Runlevel: {runlevel.split()[1]}" if runlevel else "No se pudo obtener el runlevel"
    except Exception as e:
        return f"Error al obtener el runlevel: {str(e)}"

def check_cpu_support():
    """Verifica si la CPU soporta NX/PAE."""
    try:
        cpu_info = subprocess.getoutput("cat /proc/cpuinfo")
        nx_support = "NX" if "nx" in cpu_info.lower() else "No NX support"
        pae_support = "PAE" if "pae" in cpu_info.lower() else "No PAE support"
        return f"CPU Support: {nx_support}, {pae_support}"
    except Exception as e:
        return f"Error al verificar soporte de CPU: {str(e)}"

def check_kernel_type():
    """Verifica el tipo de kernel."""
    try:
        kernel_type = subprocess.getoutput("uname -s")
        return f"Kernel Type: {kernel_type}"
    except Exception as e:
        return f"Error al obtener el tipo de kernel: {str(e)}"

def check_io_scheduler():
    """Verifica el planificador de I/O por defecto."""
    try:
        scheduler = subprocess.getoutput("cat /sys/block/sda/queue/scheduler")
        return f"Default I/O Scheduler: {scheduler}"
    except Exception as e:
        return f"Error al verificar el planificador de I/O: {str(e)}"

def check_kernel_updates():
    """Verifica si hay actualizaciones disponibles para el kernel."""
    try:
        updates = subprocess.getoutput("apt list --upgradable")
        return "Kernel updates available" if "linux-image" in updates else "No kernel updates"
    except Exception as e:
        return f"Error al verificar actualizaciones del kernel: {str(e)}"

def check_core_dumps():
    """Verifica la configuración de los volúmenes de núcleo (core dumps)."""
    try:
        limits_conf = subprocess.getoutput("grep hard /etc/security/limits.conf")
        return f"Core Dumps: {limits_conf}" if limits_conf else "No se encontraron configuraciones de core dumps"
    except Exception as e:
        return f"Error al verificar core dumps: {str(e)}"

def check_reboot_needed():
    """Verifica si se necesita reiniciar el sistema."""
    try:
        reboot_needed = subprocess.getoutput("cat /var/run/reboot-required")
        return "Reboot is required" if reboot_needed else "No reboot required"
    except Exception as e:
        return f"Error al verificar si se necesita reiniciar: {str(e)}"

def run():
    """Ejecuta todas las auditorías del kernel y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Kernel Audit] Iniciando auditoría del kernel...")

    kernel_version = get_kernel_version()
    aslr_status = check_aslr()
    kernel_parameters = check_kernel_parameters()
    loaded_kernel_modules = check_kernel_modules()
    kernel_hardening = check_kernel_hardening()
    runlevel = check_runlevel()
    cpu_support = check_cpu_support()
    kernel_type = check_kernel_type()
    io_scheduler = check_io_scheduler()
    kernel_updates = check_kernel_updates()
    core_dumps = check_core_dumps()
    reboot_needed = check_reboot_needed()

    print("\n---------------------------------------------------")
    print(f"- Kernel Version: {kernel_version}")
    print(f"- ASLR Status: {aslr_status}")
    print("- Kernel Parameters:")
    for param, data in kernel_parameters.items():
        print(f"  - {param}: {data['value']} ({data['description']})")
    print("- Loaded Kernel Modules:")
    print("  ", ", ".join(loaded_kernel_modules["loaded_modules"]))
    print(f"- Flagged Modules: {loaded_kernel_modules['flagged_modules']}")
    print("- Kernel Hardening:")
    for param, data in kernel_hardening.items():
        print(f"  - {param}: {data['value']} ({data['description']})")
    print(f"- Runlevel: {runlevel}")
    print(f"- CPU Support: {cpu_support}")
    print(f"- Kernel Type: {kernel_type}")
    print(f"- Default I/O Scheduler: {io_scheduler}")
    print(f"- Kernel Updates: {kernel_updates}")
    print(f"- Core Dumps: {core_dumps}")
    print(f"- Reboot Needed: {reboot_needed}")
    print("---------------------------------------------------\n")
    
    return {
        "kernel_version": kernel_version,
        "aslr_status": aslr_status,
        "kernel_parameters": kernel_parameters,
        "loaded_kernel_modules": loaded_kernel_modules,
        "kernel_hardening": kernel_hardening,
        "runlevel": runlevel,
        "cpu_support": cpu_support,
        "kernel_type": kernel_type,
        "io_scheduler": io_scheduler,
        "kernel_updates": kernel_updates,
        "core_dumps": core_dumps,
        "reboot_needed": reboot_needed
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
