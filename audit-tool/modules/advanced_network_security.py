import subprocess

def check_iptables_rules():
    """Verifica las reglas de iptables y si permiten tráfico no deseado."""
    try:
        # Obtiene las reglas activas de iptables
        iptables_rules = subprocess.getoutput("sudo iptables -L -n")
        
        if "ACCEPT" in iptables_rules:
            return "iptables: [Rule(s) allowing traffic found, review needed]"
        else:
            return "iptables: [No suspicious rules found]"
    except Exception as e:
        return f"Error al verificar reglas de iptables: {str(e)}"

def check_ufw_status():
    """Verifica el estado de UFW (Uncomplicated Firewall)."""
    try:
        ufw_status = subprocess.getoutput("sudo ufw status verbose")
        if "Status: active" in ufw_status:
            return "UFW: [ACTIVE] with rules applied"
        else:
            return "UFW: [INACTIVE] or no rules"
    except Exception as e:
        return f"Error al verificar el estado de UFW: {str(e)}"

def check_vpn_usage():
    """Verifica si se está utilizando una VPN o mecanismos de seguridad de red."""
    try:
        # Verifica si hay interfaces de VPN activas
        vpn_status = subprocess.getoutput("ip a | grep tun")
        if vpn_status:
            return "VPN: [Active VPN interface found]"
        else:
            return "VPN: [No active VPN interfaces found]"

    except Exception as e:
        return f"Error al verificar el uso de VPN: {str(e)}"

def check_ipsec_usage():
    """Verifica si se está utilizando IPSec para la seguridad de red."""
    try:
        # Comprobamos si hay túneles IPSec configurados
        ipsec_status = subprocess.getoutput("ip xfrm state")
        if ipsec_status:
            return "IPSec: [Active IPSec configurations found]"
        else:
            return "IPSec: [No IPSec configurations found]"
    
    except Exception as e:
        return f"Error al verificar IPSec: {str(e)}"

def run():
    """Ejecuta todas las auditorías de seguridad de red y devuelve los resultados."""
    print("\n---------------------------------------------------")
    print("[Advanced Network Security] Iniciando auditoría de seguridad de red avanzada...")

    iptables_result = check_iptables_rules()
    ufw_status = check_ufw_status()
    vpn_status = check_vpn_usage()
    ipsec_status = check_ipsec_usage()

    print("\n---------------------------------------------------")
    print(f"- iptables rules: {iptables_result}")
    print(f"- UFW status: {ufw_status}")
    print(f"- VPN usage: {vpn_status}")
    print(f"- IPSec usage: {ipsec_status}")
    print("---------------------------------------------------\n")

    return {
        "iptables_rules": iptables_result,
        "ufw_status": ufw_status,
        "vpn_status": vpn_status,
        "ipsec_status": ipsec_status
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
