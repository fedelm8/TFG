import subprocess

def check_disk_encryption():
    """Verifica si el cifrado de discos (LUKS) está habilitado en los discos críticos."""
    try:
        # Verificar si los discos están cifrados con LUKS
        encrypted_disks = subprocess.getoutput("lsblk -f | grep luks")
        if encrypted_disks:
            return f"Disk encryption enabled: {encrypted_disks}"
        else:
            return "No disk encryption enabled.\nIt's important to encrypt sensitive data disks to prevent unauthorized access."
    except Exception as e:
        return f"Error checking disk encryption: {str(e)}"

def check_mount_options():
    """Verifica que los dispositivos no estén montados con opciones inseguras."""
    try:
        # Verificar los dispositivos montados y sus opciones
        mounted_devices = subprocess.getoutput("mount | grep -v 'type'")  # Ignorar encabezados de tipo
        insecure_mounts = []
        for line in mounted_devices.splitlines():
            # Verificar si hay opciones inseguras, como 'noexec', 'nosuid', 'nodev'
            if 'noexec' in line or 'nosuid' in line or 'nodev' in line:
                insecure_mounts.append(line)
        
        if insecure_mounts:
            return f"Insecure mount options found: {', '.join(insecure_mounts)}"
        else:
            return "All mounted devices are using secure options."
    except Exception as e:
        return f"Error checking mount options: {str(e)}"

def check_disk_health():
    """Verifica el estado de los discos y la integridad del sistema de archivos."""
    try:
        # Verificar el estado de los discos usando el comando 'smartctl' (requiere 'smartmontools' instalado)
        disk_health = subprocess.getoutput("smartctl --all /dev/sda")  # Puedes cambiar '/dev/sda' a otros dispositivos
        if "SMART Health Status" in disk_health and "PASSED" in disk_health:
            return "Disk health is good."
        else:
            return "Disk health check failed or disk needs attention."
    except Exception as e:
        return f"Error checking disk health: {str(e)}"

def check_filesystem_integrity():
    """Verifica la integridad del sistema de archivos (usando fsck)."""
    try:
        # Verificar la integridad del sistema de archivos en /dev/sda1 (puedes cambiar a otros dispositivos)
        fs_check = subprocess.getoutput("sudo fsck -n /dev/sda1")
        if "clean" in fs_check:
            return "Filesystem integrity is OK."
        else:
            return "Filesystem errors found or need checking."
    except Exception as e:
        return f"Error checking filesystem integrity: {str(e)}"

def run():
    """Ejecuta todas las auditorías de dispositivos de almacenamiento y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Storage Device Security] Starting storage device audit...")

    disk_encryption = check_disk_encryption()
    mount_options = check_mount_options()
    disk_health = check_disk_health()
    fs_integrity = check_filesystem_integrity()

    print("\n---------------------------------------------------")
    print(f"- Disk Encryption: {disk_encryption}")
    print(f"- Mount Options: {mount_options}")
    print(f"- Disk Health: {disk_health}")
    print(f"- Filesystem Integrity: {fs_integrity}")
    print("---------------------------------------------------\n")

    return {
        "disk_encryption": disk_encryption,
        "mount_options": mount_options,
        "disk_health": disk_health,
        "fs_integrity": fs_integrity
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
