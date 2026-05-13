#  ExfilGuard

A real-time **file system and network exfiltration detection tool** with a GUI dashboard, Discord alerting, and multi-threaded monitoring. Built for security-conscious environments to detect suspicious file operations and outbound network activity.

---

##  Objective

The goal of ExfilGuard is to simulate and detect suspicious file and network activity in real time within a controlled environment. The project focuses on monitoring sensitive file operations, identifying potentially malicious outbound traffic, and generating live alerts through a centralized GUI dashboard and Discord webhook integration.

This project was designed to strengthen practical skills in:

- File system monitoring
- Network traffic analysis
- Real-time alerting systems
- Security event logging
- Python-based cybersecurity tool development
- GUI application development for security operations

---

##  Preview

> Dark-themed control panel with live alert feed, event legend, and one-click monitor controls.

---

##  Skills Learned

- Practical understanding of real-time file system monitoring
- Packet sniffing and network traffic inspection using Scapy
- Detection logic for suspicious outbound communications
- Multi-threaded application development in Python
- GUI design and event-driven programming using Tkinter
- Logging and alert management for security events
- Secure project structuring and GitHub repository management
- Working with Discord webhooks for automated notifications
- Basic SOC-style monitoring workflow simulation

---

##  Tools & Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Watchdog | File system event monitoring |
| Scapy | Packet sniffing and network analysis |
| Tkinter | Graphical user interface |
| Pillow (PIL) | GUI image handling |
| Requests | Webhook communication |
| Discord Webhooks | Real-time alert delivery |
| Git & GitHub | Version control and project hosting |
| Kali Linux | Testing and development environment |

---

##  Features

-  **File Monitoring** — Detects Created, Modified, Deleted, Moved, Renamed, and Copied file events
-  **Network Monitoring** — Sniffs packets and flags traffic to blacklisted IPs or suspicious ports (FTP, SSH, Telnet, proxy)
-  **Discord Alerts** — Sends real-time webhook notifications for every detected event
-  **GUI Dashboard** — Tkinter-based control panel with live alert feed, colour-coded by event type
-  **Log Management** — View, export, and clear logs from within the GUI
-  **Authentication** — Login system with admin-gated controls for starting/stopping monitoring

---

##  Project Structure

```
exfilguard/
├── exfilguard_gui.py        # Main GUI — login, dashboard, log viewer
├── exfilguard_launcher.py   # Lightweight launcher (optional entry point)
├── feds_main.py             # Orchestrator — starts file + network monitor threads
├── file_monitor.py          # Watchdog-based file system event handler
├── net_monitor.py           # Scapy-based packet sniffer
├── bg.png                   # Background image for the dashboard
└── requirements.txt
```

---

##  Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/exfilguard.git
cd exfilguard
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure before running

Open `exfilguard_gui.py` and set your admin password:

```python
ADMIN_PASSWORD = "your_secure_password"
```

Open `file_monitor.py` and `net_monitor.py`, then paste your Discord webhook URL:

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/your/webhook"
```

### 5. Run

```bash
python exfilguard_gui.py
```

> Network monitoring requires root/admin privileges for packet sniffing.
> The GUI launches `feds_main.py` with `sudo` automatically when you click **Start Monitoring**.

---

##  Discord Webhook Setup

1. Open your Discord server settings
2. Go to **Integrations → Webhooks → New Webhook**
3. Copy the webhook URL
4. Paste it into `file_monitor.py` and `net_monitor.py` as `WEBHOOK_URL`

---

##  Event Types

| Tag | Meaning |
|---|---|
| `[CREATED]` | New file detected |
| `[MODIFIED]` | File content or attributes changed |
| `[DELETED]` | File removed |
| `[MOVED]` | File moved to a different directory |
| `[RENAMED]` | File renamed within the same directory |
| `[COPIED]` | Copy operation detected |
| `[NETWORK]` | Suspicious outbound packet |

---

##  Configuration

| Setting | File | Default | Description |
|---|---|---|---|
| `ADMIN_PASSWORD` | `exfilguard_gui.py` | — | Password to start/stop monitoring |
| `WEBHOOK_URL` | `file_monitor.py`, `net_monitor.py` | — | Discord webhook for alerts |
| `INTERFACE` | `net_monitor.py` | `eth0` | Network interface to sniff |
| `blacklist_ips` | `net_monitor.py` | `["192.168.1.100"]` | IPs to flag |
| `suspicious_ports` | `net_monitor.py` | `[21, 22, 23, 8080]` | Ports to flag |
| Monitored path | `file_monitor.py` | `/home/kali/Documents` | Directory to watch |

---

##  Dependencies

See `requirements.txt`. Key packages:

- [`watchdog`](https://pypi.org/project/watchdog/) — file system event monitoring
- [`scapy`](https://scapy.net/) — packet sniffing
- [`Pillow`](https://pypi.org/project/Pillow/) — GUI background image handling
- [`requests`](https://pypi.org/project/requests/) — Discord webhook communication

---

##  License

MIT License — see `LICENSE` for details.
