import time
import re
import os

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
                    print('\a')  # plays a beep sound (optional)
                    # If you have alarm.mp3:
                    # os.system("mpg123 monitor/alarm.mp3 > /dev/null 2>&1")
                else:
                    print(f"[~] {line}")

    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
    except KeyboardInterrupt:
        print("\n[!] Monitoring stopped by user.")
