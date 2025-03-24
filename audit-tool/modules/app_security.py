import subprocess
import json

def check_apache_security():
    """Verifica la configuración de seguridad de Apache."""
    try:
        # Verifica si el módulo SSL está habilitado en Apache
        ssl_module = subprocess.getoutput("apachectl -M | grep ssl")
        if ssl_module:
            ssl_status = "SSL module enabled"
        else:
            ssl_status = "SSL module not enabled"

        # Verifica si Apache está escuchando en el puerto 443 (HTTPS)
        ssl_port = subprocess.getoutput("ss -tuln | grep :443")
        if ssl_port:
            ssl_status += " and listening on port 443"
        else:
            ssl_status += " but not listening on port 443"
        
        return f"Apache SSL/TLS Status: {ssl_status}"

    except Exception as e:
        return f"Error al verificar configuración de Apache: {str(e)}"

def check_nginx_security():
    """Verifica la configuración de seguridad de Nginx."""
    try:
        # Verifica si Nginx tiene habilitado SSL en su configuración
        ssl_config = subprocess.getoutput("grep ssl /etc/nginx/nginx.conf")
        if ssl_config:
            return "Nginx SSL/TLS is enabled"
        else:
            return "Nginx SSL/TLS is not enabled"
    
    except Exception as e:
        return f"Error al verificar configuración de Nginx: {str(e)}"

def check_mysql_security():
    """Verifica la configuración de seguridad de MySQL."""
    try:
        # Verifica si MySQL tiene habilitada la opción de conexiones seguras
        secure_connections = subprocess.getoutput("mysql -e 'SHOW VARIABLES LIKE \"have_openssl\";'")
        if "YES" in secure_connections:
            ssl_status = "SSL enabled"
        else:
            ssl_status = "SSL not enabled"

        # Verifica si MySQL tiene configurado un usuario 'root' con acceso remoto
        root_access = subprocess.getoutput("mysql -e 'SELECT host, user FROM mysql.user WHERE user=\"root\";'")
        if "localhost" in root_access:
            root_access_status = "Root access limited to localhost"
        else:
            root_access_status = "Root access is not limited to localhost"
        
        return f"MySQL SSL Status: {ssl_status}, Root access: {root_access_status}"

    except Exception as e:
        return f"Error al verificar configuración de MySQL: {str(e)}"

def check_postgresql_security():
    """Verifica la configuración de seguridad de PostgreSQL."""
    try:
        # Verifica si PostgreSQL tiene habilitada la opción de conexiones seguras (SSL)
        ssl_status = subprocess.getoutput("psql -c 'SHOW ssl;'")
        if "on" in ssl_status:
            ssl_status = "SSL enabled"
        else:
            ssl_status = "SSL not enabled"

        # Verifica si PostgreSQL tiene configurado un usuario 'postgres' con acceso remoto
        remote_access = subprocess.getoutput("psql -c \"SELECT usename, host FROM pg_stat_activity WHERE usename='postgres';\"")
        if "localhost" in remote_access:
            remote_access_status = "Postgres access limited to localhost"
        else:
            remote_access_status = "Postgres access is not limited to localhost"
        
        return f"PostgreSQL SSL Status: {ssl_status}, Remote access: {remote_access_status}"

    except Exception as e:
        return f"Error al verificar configuración de PostgreSQL: {str(e)}"

def check_ssl_configurations():
    """Verifica la configuración de SSL/TLS en los servidores web y servicios."""
    try:
        # Verifica configuraciones de SSL en Apache y Nginx
        apache_ssl = check_apache_security()
        nginx_ssl = check_nginx_security()

        # Verifica la existencia de certificados SSL
        ssl_certificates = subprocess.getoutput("ls /etc/ssl/certs")
        if ssl_certificates:
            ssl_status = "SSL certificates found"
        else:
            ssl_status = "No SSL certificates found"

        return f"{apache_ssl}, {nginx_ssl}, {ssl_status}"

    except Exception as e:
        return f"Error al verificar configuraciones SSL: {str(e)}"

def run():
    """Ejecuta todas las auditorías de seguridad de aplicaciones y devuelve los resultados."""
    print("[Application Security] Iniciando auditoría de seguridad de aplicaciones...")

    apache_security = check_apache_security()
    nginx_security = check_nginx_security()
    mysql_security = check_mysql_security()
    postgresql_security = check_postgresql_security()
    ssl_configurations = check_ssl_configurations()

    print("\n---------------------------------------------------")
    print(f"- Apache security: {apache_security}")
    print(f"- Nginx security: {nginx_security}")
    print(f"- MySQL security: {mysql_security}")
    print(f"- PostgreSQL security: {postgresql_security}")
    print(f"- SSL/TLS Configurations: {ssl_configurations}")
    print("---------------------------------------------------\n")

    return {
        "apache_security": apache_security,
        "nginx_security": nginx_security,
        "mysql_security": mysql_security,
        "postgresql_security": postgresql_security,
        "ssl_configurations": ssl_configurations
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
