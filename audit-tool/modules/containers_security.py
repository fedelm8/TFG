import subprocess
import json


def check_docker_container_configuration():
    """Verifica la configuración de los contenedores Docker."""
    try:
        # Comprobar contenedores en ejecución
        containers_running = subprocess.getoutput("docker ps")
        if "CONTAINER ID" in containers_running:
            containers = containers_running.splitlines()[1:]  # Ignorar encabezado
            container_info = []
            for container in containers:
                container_id = container.split()[0]
                container_ports = subprocess.getoutput(f"docker port {container_id}")
                container_resources = subprocess.getoutput(f"docker inspect {container_id} --format '{{{{.HostConfig.Memory}}}}")
                
                container_info.append({
                    "container_id": container_id,
                    "ports": container_ports,
                    "memory_limit": container_resources
                })
            
            return container_info
        else:
            return "No Docker containers running."  
    except Exception as e:
        return f"Error al verificar configuración de contenedores Docker: {str(e)}"

def check_lxc_container_configuration():
    """Verifica la configuración de los contenedores LXC."""
    try:
        # Comprobar contenedores LXC en ejecución
        containers_running = subprocess.getoutput("lxc list")
        if "NAME" in containers_running:
            containers = containers_running.splitlines()[1:]  # Ignorar encabezado
            container_info = []
            for container in containers:
                container_name = container.split()[0]
                container_config = subprocess.getoutput(f"lxc config show {container_name}")
                container_info.append({
                    "container_name": container_name,
                    "config": container_config
                })
            
            return container_info
        else:
            return "No LXC containers running."
    except Exception as e:
        return f"Error al verificar configuración de contenedores LXC: {str(e)}"

def check_container_images_sources():
    """Verifica que las imágenes de contenedor provengan de fuentes confiables."""
    try:
        # Comprobar imágenes de Docker
        docker_images = subprocess.getoutput("docker images")
        if "REPOSITORY" in docker_images:
            images = docker_images.splitlines()[1:]  # Ignorar encabezado
            untrusted_images = []
            for image in images:
                image_repo = image.split()[0]
                # Verifica si la imagen proviene de una fuente confiable
                if "official" not in image_repo:
                    untrusted_images.append(image_repo)
            
            if untrusted_images:
                return f"Untrusted Docker images: {', '.join(untrusted_images)}"
            else:
                return "All Docker images are from trusted sources."
        else:
            return "No Docker images found."
    except Exception as e:
        return f"Error al verificar las fuentes de las imágenes de Docker: {str(e)}"

def check_container_vulnerabilities():
    """Verifica si las imágenes de contenedores tienen vulnerabilidades conocidas."""
    try:
        # Comprobar vulnerabilidades en las imágenes de Docker usando un escáner de vulnerabilidades
        vulnerability_scan = subprocess.getoutput("docker scan --all")
        if "Vulnerabilities found" in vulnerability_scan:
            return "Vulnerabilities found in Docker images."
        else:
            return "No vulnerabilities found in Docker images."
    except Exception as e:
        return f"Error al verificar vulnerabilidades de contenedores: {str(e)}"

def run():
    """Ejecuta todas las auditorías de seguridad en contenedores y devuelve los resultados."""
    print("[Containers Security] Iniciando auditoría de seguridad en contenedores...")

    # Comprobación de configuración de contenedores Docker
    docker_configuration = check_docker_container_configuration()
    lxc_configuration = check_lxc_container_configuration()

    # Comprobación de imágenes de contenedores
    images_sources = check_container_images_sources()
    
    # Comprobación de vulnerabilidades de imágenes de contenedores
    vulnerabilities = check_container_vulnerabilities()

    print("\n---------------------------------------------------")
    print(f"- Docker container configuration: {docker_configuration}")
    print(f"- LXC container configuration: {lxc_configuration}")
    print(f"- Container image sources: {images_sources}")
    print(f"- Container vulnerabilities: {vulnerabilities}")
    print("---------------------------------------------------\n")

    return {
        "docker_configuration": docker_configuration,
        "lxc_configuration": lxc_configuration,
        "images_sources": images_sources,
        "vulnerabilities": vulnerabilities
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
