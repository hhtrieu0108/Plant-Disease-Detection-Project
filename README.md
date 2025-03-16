# Plant Diseases Detection

# Cloud Virtual Machine Setup and Configuration

## 1. Create a Virtual Machine (VM)

### 1.1 Select VM Configuration
- **Resource Group**: Choose an appropriate resource group.
- **VM Name**: Define a suitable name for the virtual machine.
- **Region**: Select `UK-South` (chosen due to student subscription availability).
- **Availability Zone**: Choose `Zone 1` (sufficient for a simple VM).
- **Image**: Select `Debian` (lightweight operating system).
- **Size**: Choose `Standard_D2s_v3` for minimal cost (suitable for small-scale usage).
- **Authentication Method**: Use `password` for ease of access.
- **Inbound Ports**: Configure ports for public access.
- **OS Disk**: Default size of `30GB` (adjust based on requirements).
- **Networking**: Use the default subnet and network settings.

### 1.2 Create the VM
After selecting the above configurations, proceed with the VM creation.

---

## 2. Connect to the Virtual Machine

### 2.1 Access the VM
- Navigate to the **Azure Portal**.
- Open the **Virtual Machine Resource**.
- Click on **Connect**.
- Select **SSH using Azure CLI** (recommended for web browser access).
- Click **Configure + Connect**, then initiate the connection.

### 2.2 Establish SSH Connection
Execute the following command in the Azure Cloud Shell or local terminal:
```sh
ssh <username>@<public-ip>
```
Example:
```sh
ssh dat-fptu@20.90.90.19
```

---

## 3. Environment Setup

### 3.1 Verify Python Installation
Debian includes Python by default. Verify using:
```sh
python3 --version
```

### 3.2 Install Git
Install Git using the following command:
```sh
sudo apt install git -y
```

### 3.3 Clone the Project Repository
```sh
git clone <repository-url>
cd <repository-directory>
```

### 3.4 Setup Python Virtual Environment
Install `python3.11-venv` if not already available:
```sh
sudo apt install python3.11-venv -y
```

Create and activate a virtual environment:
```sh
python3 -m venv venv
source ./venv/bin/activate
```

### 3.5 Install Required Dependencies
```sh
pip install -r requirements.txt
```

### 3.6 Configure Network for Public Access on Port 5000
- Navigate to **VM Network Settings** in Azure Portal.
- Open **Inbound Port Rules**.
- Add a rule for **Port 5000** with **TCP Protocol**.

---

## 4. Run the Application

Execute the following command to start the application:
```sh
python3 app.py
```

The application should now be accessible via the configured public IP on port `5000`.

---

## Notes
- Ensure firewall settings allow external access if required.
- Update dependencies periodically using:
  ```sh
  pip install --upgrade -r requirements.txt
  ```
- For security, consider using SSH key-based authentication instead of passwords.
