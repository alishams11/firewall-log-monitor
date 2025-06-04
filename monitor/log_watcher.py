import time

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
                print(line.strip())
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
    except KeyboardInterrupt:
        print("\n[!] Monitoring stopped by user.")
