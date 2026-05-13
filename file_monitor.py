from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging
import requests
import os
import hashlib
from datetime import datetime

# Discord Webhook
# Create your webhook at: Discord Server Settings > Integrations > Webhooks
# Paste your webhook URL below
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def send_discord_alert(message):
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("⚠ Discord webhook URL not configured.", flush=True)
        return

    data = {"content": message}

    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print("📬 Discord response code:", response.status_code, flush=True)

        if response.status_code != 204:
            print("⚠ Discord response text:", response.text, flush=True)

    except Exception as e:
        print("❌ Exception while sending to Discord:", e, flush=True)

# Logging
logging.basicConfig(
    filename="feds.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Store file hashes to detect modifications
file_hashes = {}
file_sizes = {}

def get_file_hash(filepath):
    """Calculate MD5 hash of a file to detect modifications"""
    try:
        if not os.path.isfile(filepath):
            return None

        hash_md5 = hashlib.md5()

        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    except (IOError, OSError):
        return None

def get_file_info(filepath):
    """Get file size and modification time"""
    try:
        stat = os.stat(filepath)
        return stat.st_size, stat.st_mtime

    except (OSError, IOError):
        return None, None

# Event handler with enhanced monitoring
class FileMonitor(FileSystemEventHandler):

    def __init__(self):
        super().__init__()
        self.last_created_file = None
        self.last_created_time = None

    def on_modified(self, event):
        if not event.is_directory:

            filepath = event.src_path

            # Get current file info
            current_size, current_mtime = get_file_info(filepath)
            current_hash = get_file_hash(filepath)

            # Check if file was previously known
            if filepath in file_hashes:

                old_hash = file_hashes[filepath]
                old_size = file_sizes.get(filepath, {}).get('size', 0)

                # If hash changed, it's a modification
                if current_hash and old_hash and current_hash != old_hash:

                    msg = f"[MODIFIED] Content changed: {filepath} (Size: {old_size} → {current_size} bytes)"

                    logging.info(msg)
                    send_discord_alert(msg)

                    print("📝", msg, flush=True)

                # Update stored hash and size
                if current_hash:
                    file_hashes[filepath] = current_hash
                    file_sizes[filepath] = {
                        'size': current_size,
                        'mtime': current_mtime
                    }

            else:
                # First time seeing this file modification
                if current_hash:

                    file_hashes[filepath] = current_hash

                    file_sizes[filepath] = {
                        'size': current_size,
                        'mtime': current_mtime
                    }

                    msg = f"[MODIFIED] File attributes changed: {filepath}"

                    logging.info(msg)
                    send_discord_alert(msg)

                    print("📝", msg, flush=True)

    def on_created(self, event):
        if not event.is_directory:

            filepath = event.src_path

            msg = f"[CREATED] New file: {filepath}"

            logging.info(msg)
            send_discord_alert(msg)

            print("📁", msg, flush=True)

            # Store file info for future modification detection
            current_hash = get_file_hash(filepath)
            current_size, current_mtime = get_file_info(filepath)

            if current_hash:
                file_hashes[filepath] = current_hash

                file_sizes[filepath] = {
                    'size': current_size,
                    'mtime': current_mtime
                }

            # Track for potential copy detection
            self.last_created_file = filepath
            self.last_created_time = datetime.now()

    def on_deleted(self, event):
        if not event.is_directory:

            filepath = event.src_path

            msg = f"[DELETED] File removed: {filepath}"

            logging.info(msg)
            send_discord_alert(msg)

            print("🗑", msg, flush=True)

            # Remove from tracking
            if filepath in file_hashes:
                del file_hashes[filepath]

            if filepath in file_sizes:
                del file_sizes[filepath]

    def on_moved(self, event):
        if not event.is_directory:

            src_path = event.src_path
            dest_path = event.dest_path

            # This could be a move OR a rename
            src_dir = os.path.dirname(src_path)
            dest_dir = os.path.dirname(dest_path)

            if src_dir == dest_dir:

                # Same directory = rename
                msg = f"[RENAMED] {src_path} → {dest_path}"

                logging.info(msg)
                send_discord_alert(msg)

                print("✏", msg, flush=True)

            else:

                # Different directory = move
                msg = f"[MOVED] {src_path} → {dest_path}"

                logging.info(msg)
                send_discord_alert(msg)

                print("📦", msg, flush=True)

            # Update tracking for the moved/renamed file
            if src_path in file_hashes:
                file_hashes[dest_path] = file_hashes.pop(src_path)

            if src_path in file_sizes:
                file_sizes[dest_path] = file_sizes.pop(src_path)

            # Check if this might be a copy operation
            if (
                self.last_created_file and
                self.last_created_time and
                (datetime.now() - self.last_created_time).total_seconds() < 2
            ):

                created_hash = get_file_hash(self.last_created_file)
                moved_hash = get_file_hash(dest_path)

                if created_hash and moved_hash and created_hash == moved_hash:

                    msg = f"[COPIED] File copied: {self.last_created_file} → {dest_path}"

                    logging.info(msg)
                    send_discord_alert(msg)

                    print("📋", msg, flush=True)

            self.last_created_file = None
            self.last_created_time = None

def start_file_monitoring(path="/home/kali/Documents"):
    """Start file monitoring on specified path"""

    print(f"📁 File monitoring started on {path}")

    observer = Observer()
    event_handler = FileMonitor()

    observer.schedule(event_handler, path=path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_file_monitoring()
