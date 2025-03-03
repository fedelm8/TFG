import subprocess

def check_system_binaries():
    """Verifica si los binarios necesarios existen en los directorios especificados."""
    directories = ['/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/local/bin']
    results = {}
    for directory in directories:
        try:
            result = subprocess.getoutput(f"ls {directory}")
            results[directory] = "FOUND" if result else "NOT FOUND"
        except Exception as e:
            results[directory] = f"Error: {str(e)}"
    return results

def check_pam():
    """Verifica si el módulo PAM está instalado."""
    try:
        pam_status = subprocess.getoutput("ls /etc/pam.d")
        return "FOUND" if pam_status else "NOT FOUND"
    except Exception as e:
        return f"Error al verificar PAM: {str(e)}"

def check_debian_tests():
    """Verifica la ejecución de pruebas de Debian y sus resultados."""
    try:
        test_results = subprocess.getoutput("debian-tests")
        # Suponiendo que `debian-tests` es un comando que realiza la prueba.
        if "DEB-0001" in test_results:
            return "Test executed successfully"
        else:
            return "Test did not execute as expected"
    except Exception as e:
        return f"Error al ejecutar pruebas de Debian: {str(e)}"

def check_required_packages():
    """Verifica si los paquetes esenciales están instalados."""
    packages = ['libpam-tmpdir', 'apt-listbugs', 'apt-listchanges', 'needrestart', 'fail2ban']
    results = {}
    for package in packages:
        try:
            check = subprocess.getoutput(f"dpkg -l | grep {package}")
            results[package] = "Installed" if check else "Not Installed"
        except Exception as e:
            results[package] = f"Error: {str(e)}"
    return results

def check_filesystem_checks():
    """Verifica la instalación de herramientas de verificación del sistema de archivos."""
    try:
        check_dmcrypt = subprocess.getoutput("which dmcrypt")
        check_cryptsetup = subprocess.getoutput("which cryptsetup")
        check_cryptmount = subprocess.getoutput("which cryptmount")
        
        return {
            "DM-Crypt": "Found" if check_dmcrypt else "Not Found",
            "Cryptsetup": "Found" if check_cryptsetup else "Not Found",
            "Cryptmount": "Found" if check_cryptmount else "Not Found"
        }
    except Exception as e:
        return f"Error al verificar herramientas de sistema de archivos: {str(e)}"

def run():
    """Ejecuta todas las pruebas relacionadas con Debian y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Debian Tests] Iniciando prueba de Debian...")

    system_binaries = check_system_binaries()
    pam_status = check_pam()
    debian_test_results = check_debian_tests()
    required_packages = check_required_packages()
    filesystem_checks = check_filesystem_checks()

    print("\n---------------------------------------------------")
    print("[System Binaries Required by Debian Tests]")
    for directory, result in system_binaries.items():
        print(f"  - Checking {directory}: {result}")
    
    print(f"- Authentication (PAM): {pam_status}")
    print(f"- Debian Tests: {debian_test_results}")
    
    print("[File System Checks]")
    for tool, result in filesystem_checks.items():
        print(f"  - {tool}: {result}")
    
    print("[Required Software Packages]")
    for package, status in required_packages.items():
        print(f"  - {package}: {status}")
    
    print("---------------------------------------------------\n")

    return {
        "system_binaries": system_binaries,
        "pam_status": pam_status,
        "debian_test_results": debian_test_results,
        "required_packages": required_packages,
        "filesystem_checks": filesystem_checks
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
