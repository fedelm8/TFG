import subprocess

def check_sudo_access():
    """Checks sudo usage to ensure users have only necessary access."""
    try:
        # List users with sudo privileges
        sudo_users = subprocess.getoutput("getent group sudo")
        if sudo_users:
            users = sudo_users.split(":")[-1].split(",")
            return f"Users with sudo access: {', '.join(users)}.\nEnsure that only authorized users have sudo access."
        else:
            return "No users with sudo access found.\nThis indicates no users have sudo access configured."
    except Exception as e:
        return f"Error checking sudo access: {str(e)}"

def check_sudoers_file():
    """Audits the /etc/sudoers file for unsafe configurations or excessive permissions."""
    try:
        # Check permissions of the sudoers file
        sudoers_permissions = subprocess.getoutput("ls -l /etc/sudoers")
        if sudoers_permissions:
            if "root root" in sudoers_permissions and "440" in sudoers_permissions:
                sudoers_status = "Sudoers file permissions are correct (root:root, 440)."
            else:
                sudoers_status = "Sudoers file permissions are incorrect.\nThe file should have 440 permissions and be owned by root."
        else:
            sudoers_status = "Sudoers file not found.\nThis is a critical issue, as the sudoers file is essential for sudo configuration."
        
        # Check if the sudoers file has syntax errors
        sudoers_config = subprocess.getoutput("sudo visudo -c")
        if "syntax OK" in sudoers_config:
            sudoers_config_status = "Sudoers file is syntactically correct."
        else:
            sudoers_config_status = "Sudoers file has syntax errors.\nFix syntax issues to avoid misconfigurations."

        return sudoers_status + " " + sudoers_config_status
    except Exception as e:
        return f"Error auditing /etc/sudoers: {str(e)}"

def check_sudoers_inclusions():
    """Checks if dangerous inclusions exist in the sudoers file."""
    try:
        sudoers_inclusions = subprocess.getoutput("grep -i 'include' /etc/sudoers")
        if "includedir" in sudoers_inclusions:
            return "Included directories found in sudoers file.\nBe cautious with included directories as they may introduce untrusted configurations."
        else:
            return "No included directories found in sudoers file.\nThis is a good practice to avoid untrusted configurations."
    except Exception as e:
        return f"Error checking inclusions in sudoers: {str(e)}"

def run():
    """Runs all elevated privilege audits and returns the results."""
    print("\n---------------------------------------------------")
    print("[Sudo Privileges] Starting sudo privilege audit...")

    sudo_access = check_sudo_access()
    sudoers_file = check_sudoers_file()
    sudoers_inclusions = check_sudoers_inclusions()

    print("\n---------------------------------------------------")
    print(f"- Sudo access: {sudo_access}")
    print(f"- Sudoers file configuration: {sudoers_file}")
    print(f"- Sudoers inclusions: {sudoers_inclusions}")
    print("---------------------------------------------------\n")

    return {
        "sudo_access": sudo_access,
        "sudoers_file": sudoers_file,
        "sudoers_inclusions": sudoers_inclusions
    }

if __name__ == "__main__":
    output = run()
    print(json.dumps(output, indent=4))
