
# 🧰 audit_tool

*Comprehensive OS auditing in a modular and structured way.*

![Last Commit](https://img.shields.io/github/last-commit/fedelm8/TFG)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux-orange)

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation and Usage](#installation-and-usage)

---

## Overview

**audit_tool** is a robust monitoring tool designed to safeguard sensitive files by detecting unauthorized access in real-time.

### Why audit_tool?

This project enhances system security by providing continuous oversight of critical files. The core features include:

- 🔍 **Full System Auditing**: Covers system info, network, security, file system, memory, containers and more.
- 🧱 **Modular Architecture**: Easy to maintain and extend with separate scripts for each audit task.
- 🛡️ **Threat Detection**: Integration with tools like `chkrootkit` and `clamav` for malware detection.
- 📦 **Package and Kernel Checkups**: Verify updates, kernel integrity, and boot services.
- 🔐 **User & Access Control Audits**: From sudoers to service accounts, everything's inspected.

---


## Prerequisites

    -  Python 3.x  
    - `requests`  
    - `psutil`
    - `pyfiglet` 
    - `colorama`
    - `pip`
    - `git`

---


## Project Structure

```
audit_tool/
├── audit_tool.py
└── modules/
    ├── // INFORMACIÓN DEL SISTEMA
    │   ├── sys_info.py
    │   ├── kernel.py
    │   ├── boot_services.py
    │   └── updates.py
    ├── // RED Y COMUNICACIONES
    │   ├── network.py
    │   └── advanced_network_security.py
    ├── // SEGURIDAD DEL SISTEMA Y ACCESOS
    │   ├── users_groups_auth.py
    │   ├── file_permissions.py
    │   ├── sudo.py
    │   ├── service_accounts.py
    │   ├── security_policies.py
    │   └── app_security.py
    ├── // ARCHIVOS Y DIRECTORIOS
    │   ├── home_directories.py
    │   └── storage_device.py
    ├── // PROCESOS MEMORIA Y ACTIVIDAD
    │   ├── mem_process.py
    │   └── logs.py
    ├── // CONTENEDORES Y ENTORNO VISUAL
    │   └── containers_security.py
    ├── // BACKUP Y RECUPERACIÓN
    │   └── backup.py
    ├── // TESTS
    │   └── debian_tests.py
    └── // PROTECCIÓN Y DETECCIÓN DE AMENAZAS
        └── malware_protection.py
```


---

---

##  Installation and Usage

### 1. Set Up Virtual Machine

1. Download Ubuntu 24.04 Noble Numbat for VirtualBox (OVA):  
   👉 https://www.osboxes.org/ubuntu/

2. In VirtualBox, go to `File > Import Appliance`, and select the downloaded `.ova`.

3. When prompted, the user and password will be:
   ```
   username: osboxes
   password: osboxes.org
   ```

---

### 2. Install Dependencies

Open a terminal and run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip
```

Restart the VM afterwards.

---

### 3. Clone the Repository

```bash
cd ~/Documents  # or any preferred directory
git clone https://github.com/fedelm8/TFG
cd TFG  # Replace with the name of your repo if different
```

---

### 4. Set Up Python Environment

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. Install Extra Audit Tools

```bash
sudo apt install chkrootkit clamav
```

---

### 6. Run the Tool

```bash
sudo venv/bin/python audit_tool.py
```

---

