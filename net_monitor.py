from scapy.all import sniff, IP, TCP
import logging
import requests

# Discord Webhook
# Create your webhook at: Discord Server Settings > Integrations > Webhooks
# Paste your webhook URL below
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

INTERFACE = "eth0"  # Change this if your interface is different

def send_discord_alert(message):

    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("⚠ Discord webhook URL not configured.", flush=True)
        return

    data = {"content": message}

    try:
        requests.post(WEBHOOK_URL, json=data)

    except:
        pass

logging.basicConfig(
    filename="feds.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Suspicious targets only
blacklist_ips = ["192.168.1.100"]  # Example IP
suspicious_ports = [21, 22, 23, 8080]  # FTP, SSH, Telnet, proxy ports

def packet_callback(packet):

    if packet.haslayer(IP) and packet.haslayer(TCP):

        dest_ip = packet[IP].dst
        dest_port = packet[TCP].dport

        if dest_ip in blacklist_ips or dest_port in suspicious_ports:

            msg = f"[NETWORK] Suspicious packet to {dest_ip}:{dest_port}"

            logging.info(msg)
            send_discord_alert(msg)

            print(msg)  # Only print if suspicious

def start_sniffing():

    print(f"🌐 Sniffing on {INTERFACE} (Ctrl+C to stop)...")

    sniff(
        iface=INTERFACE,
        prn=packet_callback,
        store=0
    )
