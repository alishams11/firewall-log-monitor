from monitor.log_watcher import follow_log

if __name__ == "__main__":
    log_path = input("Enter path to firewall log file: ").strip()
    follow_log(log_path)
