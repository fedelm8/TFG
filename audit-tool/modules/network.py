import subprocess
import json

def check_ipv6_configuration():
    """Verifica la configuración de IPv6."""
    try:
        ipv6_status = subprocess.getoutput("sysctl net.ipv6.conf.all.disable_ipv6")
        return "Enabled" if "0" in ipv6_status else "Disabled"
    except Exception as e:
        return f"Error al verificar configuración de IPv6: {str(e)}"

def check_dns_servers():
    """Verifica los servidores DNS configurados."""
    try:
        # Extract only the nameservers from /etc/resolv.conf
        dns_servers = subprocess.getoutput("grep -i 'nameserver' /etc/resolv.conf")
        if dns_servers:
            return "OK", dns_servers.strip()
        else:
            return "Not Found", None
    except Exception as e:
        return f"Error al verificar servidores DNS: {str(e)}", None

def check_dnssec_support():
    """Verifica si DNSSEC está habilitado."""
    try:
        dnssec_status = subprocess.getoutput("systemctl is-active systemd-resolved")
        return "Enabled" if "active" in dnssec_status else "Unknown"
    except Exception as e:
        return f"Error al verificar DNSSEC: {str(e)}"

def check_default_gateway():
    """Verifica la puerta de enlace predeterminada."""
    try:
        gateway = subprocess.getoutput("ip route | grep default")
        return "OK" if gateway else "Not Found"
    except Exception as e:
        return f"Error al verificar puerta de enlace predeterminada: {str(e)}"

def get_listening_ports():
    """Obtiene los puertos de escucha (TCP/UDP)."""
    try:
        listening_ports = subprocess.getoutput("ss -tuln")
        return listening_ports if listening_ports else "Not Found"
    except Exception as e:
        return f"Error al obtener puertos de escucha: {str(e)}"

def check_promiscuous_interfaces():
    """Verifica si hay interfaces en modo promiscuo."""
    try:
        interfaces = subprocess.getoutput("ip link show | grep promisc")
        return "OK" if interfaces else "Not Found"
    except Exception as e:
        return f"Error al verificar interfaces promiscuas: {str(e)}"

def check_waiting_connections():
    """Verifica las conexiones en estado de espera."""
    try:
        waiting_connections = subprocess.getoutput("ss -tuln | grep 'SYN'")
        return "OK" if waiting_connections else "Not Found"
    except Exception as e:
        return f"Error al verificar conexiones en espera: {str(e)}"

def check_dhcp_client_status():
    """Verifica el estado del cliente DHCP."""
    try:
        dhcp_status = subprocess.getoutput("systemctl is-active dhclient")
        return "OK" if "active" in dhcp_status else "Not Found"
    except Exception as e:
        return f"Error al verificar estado del cliente DHCP: {str(e)}"

def check_arp_monitoring_software():
    """Verifica si hay software de monitoreo ARP."""
    try:
        arp_monitor = subprocess.getoutput("ps aux | grep arpwatch")
        return "Found" if arp_monitor else "Not Found"
    except Exception as e:
        return f"Error al verificar software de monitoreo ARP: {str(e)}"

def check_uncommon_network_protocols():
    """Verifica la presencia de protocolos de red poco comunes."""
    try:
        uncommon_protocols = subprocess.getoutput("netstat -tuln | grep -E 'tcp6|udp6'")
        return "Found" if uncommon_protocols else "Not Found"
    except Exception as e:
        return f"Error al verificar protocolos de red poco comunes: {str(e)}"

def run():
    """Ejecuta todas las auditorías de red y devuelve los resultados."""
    print("[Networking] Iniciando auditoría de red...")

    ipv6_status = check_ipv6_configuration()
    dns_status, dns_servers = check_dns_servers()
    dnssec_status = check_dnssec_support()
    gateway_status = check_default_gateway()
    listening_ports = get_listening_ports()
    promiscuous_interfaces = check_promiscuous_interfaces()
    waiting_connections = check_waiting_connections()
    dhcp_status = check_dhcp_client_status()
    arp_monitor_status = check_arp_monitoring_software()
    uncommon_protocols = check_uncommon_network_protocols()

    print("\n---------------------------------------------------")
    print(f"- IPv6 Configuration: {ipv6_status}")
    print(f"- DNS Servers: {dns_status}")
    if dns_status == "OK":
        print(f"  - Servers: {dns_servers}")
    print(f"- DNSSEC (systemd-resolved): {dnssec_status}")
    print(f"- Default Gateway: {gateway_status}")
    print(f"- Listening Ports (TCP/UDP): {listening_ports}")
    print(f"- Promiscuous Interfaces: {promiscuous_interfaces}")
    print(f"- Waiting Connections: {waiting_connections}")
    print(f"- DHCP Client Status: {dhcp_status}")
    print(f"- ARP Monitoring Software: {arp_monitor_status}")
    print(f"- Uncommon Network Protocols: {uncommon_protocols}")
    print("---------------------------------------------------\n")

    return {
        "ipv6_status": ipv6_status,
        "dns_status": dns_status,
        "dns_servers": dns_servers,
        "dnssec_status": dnssec_status,
        "gateway_status": gateway_status,
        "listening_ports": listening_ports,
        "promiscuous_interfaces": promiscuous_interfaces,
        "waiting_connections": waiting_connections,
        "dhcp_status": dhcp_status,
        "arp_monitor_status": arp_monitor_status,
        "uncommon_protocols": uncommon_protocols
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
