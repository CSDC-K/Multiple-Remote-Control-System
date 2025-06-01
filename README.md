# MRCS - Multiple Remote Control System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📌 Overview

**MRCS (Multiple Remote Control System)** is a Python-based application designed to manage multiple computers within the same network. It facilitates tasks such as:

* Sending messages to connected clients
* Transferring files between the admin and clients
* Sharing screens for remote assistance
* Executing remote commands

This tool is ideal for network administrators, educators, and IT professionals who require efficient control over multiple systems simultaneously.

## 🚀 Features

* **Multi-Client Management**: Control several client machines from a single admin interface.
* **Secure Communication**: Ensures data integrity and security during transmissions.
* **User-Friendly Interface**: Intuitive design for ease of use.
* **Cross-Platform Compatibility**: Operable on both Windows and Linux systems.

## 🛠️ Installation

### Prerequisites

* Python 3.8 or higher
* pip package manager

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/CSDC-K/Multiple-Remote-Control-System.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd Multiple-Remote-Control-System
   ```

3. **Install Required Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Convert Python Files to Executables (Optional)**

   If you wish to create executable files for easier deployment:

   ```bash
   pip install pyinstaller
   pyinstaller --onefile admin.py
   pyinstaller --onefile client.py
   ```

## 📂 Project Structure

```
Multiple-Remote-Control-System/
├── admin/
│   └── admin.py
├── client/
│   └── client.py
├── tools/
│   └── [Additional utility scripts]
├── README.md
└── requirements.txt
```

* **admin/**: Contains the main administrative application.
* **client/**: Houses the client-side application to be deployed on target machines.
* **tools/**: Includes supplementary scripts and tools to enhance functionality.

## ⚙️ Usage

1. **Ensure Network Connectivity**

   Both the admin and client machines should be connected to the same network.

2. **Deploy the Client Application**

   Run the `client.py` script on all machines you intend to control.

   ```bash
   python client.py
   ```

3. **Launch the Admin Application**

   On your main machine, execute the `admin.py` script to open the control interface.

   ```bash
   python admin.py
   ```

4. **Interact with Clients**

   Use the admin interface to send messages, transfer files, share screens, or execute commands on connected client machines.

## 💻 Screenshots

*Note: Include screenshots of the admin interface and client application here to provide visual context.*

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## 📧 Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/CSDC-K/Multiple-Remote-Control-System/issues).

---

Feel free to customize this README further to align with your project's specific details and requirements. If you need assistance with creating logos or additional branding materials, please let me know!
