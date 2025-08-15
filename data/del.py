import os

# List of log files to clean
log_files = [
    "/var/log/auth.log",
    "/var/log/dmesg",
    "/var/log/kern.log",
    "/var/log/syslog",
    "/var/log/Xorg.0.log"
]

for log_file in log_files:
    try:
        if os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.truncate(0)
            print(f"Cleaned: {log_file}")
        else:
            print(f"File not found: {log_file}")
    except PermissionError:
        print(f"Permission denied: {log_file} (try running as sudo)")
    except Exception as e:
        print(f"Error cleaning {log_file}: {e}")
