import os
import json
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

from concurrent.futures import ProcessPoolExecutor

def run_command(command, timeout=20):
    """Ejecuta un comando en la terminal con un límite de tiempo."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"Tiempo de espera excedido ({timeout}s)"
    except Exception as e:
        return str(e)

def system_info():
    """Obtiene información avanzada del sistema."""
    commands = {
        "OS": "lsb_release -d",
        "Kernel": "uname -r",
        "CPU Info": "lscpu | grep 'Model name'",
        "RAM Usage": "free -h",
        "Disk Usage": "df -h | grep '/$'",
        "Mounted Filesystems": "mount | column -t",
        "Running Processes": "ps aux --sort=-%mem | head -10",
        "Uptime": "uptime"
        # "Osquery System Info": "osqueryi --json 'SELECT * FROM system_info;'"  # Comentado temporalmente
    }
    
    with ProcessPoolExecutor() as executor:
        results = {key: executor.submit(run_command, cmd) for key, cmd in commands.items()}
        return {key: result.result() for key, result in results.items()}

def security_audit():
    """Ejecuta una auditoría de seguridad avanzada."""
    commands = {
        "Usuarios con sudo": "getent group sudo",
        "SSH Configuración": "cat /etc/ssh/sshd_config | grep -i permitrootlogin",
        "Lynis Security Scan": "lynis audit system",
        "Chkrootkit": "chkrootkit",
        "Rkhunter": "rkhunter --check --skip-keypress",
        "Auditd Logs": "ausearch -m avc -ts recent",
        "SELinux Status": "sestatus",
        "Debsums Integrity Check": "debsums -s",
        "ClamAV Scan": "clamscan -r / --bell --quiet"
        # "Osquery Security Audit": "osqueryi --json 'SELECT * FROM users;'"  # Comentado temporalmente
    }
    
    with ProcessPoolExecutor() as executor:
        results = {key: executor.submit(run_command, cmd, 30) for key, cmd in commands.items()}
        return {key: result.result() for key, result in results.items()}

def network_audit():
    """Auditoría de seguridad de red avanzada."""
    commands = {
        "Interfaces de red": "ip a",
        "Puertos abiertos (Nmap)": "nmap -sV -T4 -A localhost",
        "Conexiones activas": "ss -tulnp",
        "Firewall (UFW Status)": "ufw status verbose",
        "ARP Scan": "arp-scan --localnet",
        "Wireshark Analysis": "tshark -D"
    }
    
    with ProcessPoolExecutor() as executor:
        results = {key: executor.submit(run_command, cmd, 20) for key, cmd in commands.items()}
        return {key: result.result() for key, result in results.items()}

def container_audit():
    """Auditoría de contenedores y virtualización."""
    commands = {
        "Docker Containers": "docker ps -a",
        "Docker Security Scan": "docker scan $(docker images --format '{{.Repository}}')",
        "Podman Containers": "podman ps -a",
        "KVM Virtual Machines": "virsh list --all",
        "Trivy Scan": "trivy fs /"
        # "Falco Events": "falco --list"  # Comentado temporalmente
    }
    
    with ProcessPoolExecutor() as executor:
        results = {key: executor.submit(run_command, cmd, 20) for key, cmd in commands.items()}
        return {key: result.result() for key, result in results.items()}

def generate_report():
    """Genera un informe JSON consolidado."""
    report = {
        "System Info": system_info(),
        "Security Audit": security_audit(),
        "Network Audit": network_audit(),
        "Container Audit": container_audit()
    }
    with open("audit_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("Informe generado: audit_report.json")
    return report

def generate_pdf_report(report_data, filename="audit_report_advanced.pdf"):
    """Genera un informe en formato PDF con los resultados de la auditoría."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("<b>Informe de Auditoría del Sistema - Avanzado</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    for section, data in report_data.items():
        section_title = Paragraph(f"<b>{section}</b>", styles["Heading2"])
        elements.append(section_title)
        elements.append(Spacer(1, 6))
        
        table_data = [[key, str(value)] for key, value in data.items()]
        
        # Dividir la tabla si es demasiado grande
        max_rows_per_table = 20  # Ajusta esto si es necesario
        for i in range(0, len(table_data), max_rows_per_table):
            table = Table(table_data[i:i+max_rows_per_table], colWidths=[250, 250])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

            # Insertar salto de página si hay más filas
            if i + max_rows_per_table < len(table_data):
                elements.append(PageBreak())

    doc.build(elements)
    print(f"Informe PDF generado: {filename}")
    return filename


if __name__ == "__main__":
    report = generate_report()
    generate_pdf_report(report)
