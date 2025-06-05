import time
import re

# List of suspicious patterns to look for in firewall logs
SUSPICIOUS_PATTERNS = [
    r'\bDROP\b',
    r'\bREJECT\b',
    r'\bPORTSCAN\b',
    r'UFW BLOCK',
    r'\bBlocked attempt\b'
]

def is_suspicious(line):
    """
    Check if a log line matches any suspicious pattern.
    Returns True if a match is found, otherwise False.
    """
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, line):
            return True
    return False

def follow_log(file_path):
    """
    Monitor the specified log file in real-time.
    Similar to 'tail -f', it reads new lines as they are added.
    Prints an alert if any suspicious pattern is detected.
    """
    try:
        with open(file_path, 'r') as file:
            # Move to the end of the file
            file.seek(0, 2)
            print(f"[+] Monitoring {file_path} ... (Ctrl+C to stop)")

            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                line = line.strip()
                if is_suspicious(line):
                    # Print suspicious log entry in red
                    print(f"\033[91m[!] ALERT: Suspicious activity detected:\n{line}\033[0m\n")
                else:
                    print(f"[~] {line}")

    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
    except KeyboardInterrupt:
        print("\n[!] Monitoring stopped by user.")
