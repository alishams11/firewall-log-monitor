import time
import re
import os
import json
from monitor.telegram_alert import send_telegram_alert
from datetime import datetime


SUSPICIOUS_PATTERNS = [
    r'\bDROP\b',
    r'\bREJECT\b',
    r'\bPORTSCAN\b',
    r'UFW BLOCK',
    r'\bBlocked attempt\b'
]

def is_suspicious(line):
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, line):
            return True
    return False


def save_alert_to_file(ip, message):
    alert = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "message": message
    }

    alerts_file = "alerts/alerts.json"
    try:
        if not os.path.exists(alerts_file) or os.stat(alerts_file).st_size == 0:
            alerts = []
        else:
            with open(alerts_file, 'r') as f:
                alerts = json.load(f)

        alerts.append(alert)

        with open(alerts_file, 'w') as f:
            json.dump(alerts, f, indent=4)

    except Exception as e:
        print(f"[!] Failed to write alert to file: {e}")


def follow_log(file_path):
    try:
        with open(file_path, 'r') as file:
            file.seek(0, 2)
            print(f"[+] Monitoring {file_path} ... (Ctrl+C to stop)")

            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                line = line.strip()
                if is_suspicious(line):
                    print(f"\033[91m[🔥 ALERT] Suspicious activity detected:\n🚨 {line}\033[0m\n")
                    print('\a')
                    send_telegram_alert(f"🚨 Suspicious activity detected:\n{line}")
                    os.system("mpg123 monitor/alarm.mp3 > /dev/null 2>&1")
                    ip_match = re.search(r'SRC=(\d+\.\d+\.\d+\.\d+)', line)
                    ip = ip_match.group(1) if ip_match else "Unknown"
                    save_alert_to_file(ip, line)

                      # plays a beep sound (optional)
                    # If you have alarm.mp3:
                else:
                    print(f"[~] {line}")

    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
    except KeyboardInterrupt:
        print("\n[!] Monitoring stopped by user.")
    