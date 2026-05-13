import threading
import time
import logging
from file_monitor import start_file_monitoring
from net_monitor import start_sniffing

# Logging setup
logging.basicConfig(
    filename="feds.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def run_all_monitors():
    # Thread 1: File Monitor
    file_thread = threading.Thread(target=start_file_monitoring)
    file_thread.daemon = True
    file_thread.start()

    # Thread 2: Network Monitor
    net_thread = threading.Thread(target=start_sniffing)
    net_thread.daemon = True
    net_thread.start()

    print("🚨 EXFILGUARD: Enhanced File + Network Monitoring Starting...")
    print("📁 Monitoring: Created, Modified, Deleted, Moved, Renamed, Copied files")
    print("🌐 Monitoring: Network traffic on suspicious ports")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping EXFILGUARD monitoring...")

if __name__ == "__main__":
    run_all_monitors()