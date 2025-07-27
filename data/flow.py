import re 
import json
import datetime
from datetime import datetime as dt
from pathlib import Path

def json_store():
    # Current date
    date = datetime.date.today()
    op_file = f"{date}.json"

    # ✅ Custom directory paths
    store_logs = Path("/home/l0ki/darkhold/l0ki/dataflow/tdata")
    #st = Path("/home/l0ki/darkhold/dataflow")
    output_path = store_logs / op_file

    # Log patterns for each type
    log_files = {
        "auth.log.txt": r"(?P<timestamp>\d{4}-\d{2}-\d{2}T[\d:.+\-]+) (?P<host>\S+) (?P<process>[\w\-/\[\]@.]+)(:|\[\d+\]:)? (?P<message>.*)",
        "syslog.txt": r"(?P<timestamp>\d{4}-\d{2}-\d{2}T[\d:.+\-]+) (?P<host>\S+) (?P<process>[\w\-/().\[\]@]+)(\[.*?\])?: (?P<message>.*)",
        "kern.log.txt": r"(?P<timestamp>\d{4}-\d{2}-\d{2}T[\d:.+\-]+) (?P<host>\S+) kernel: (?P<message>.*)",
        "dmesg.txt": r"\[\s*(?P<timestamp>[\d.]+)] kernel: (?P<message>.*)",
        "Xorg.0.log.txt": r"\[\s*(?P<timestamp>[\d.]+)] (?P<message>.*)"
    }

    logs = {}

    # Process each file
    for file_name, pattern in log_files.items():
        file_path = store_logs / file_name
        if not file_path.exists():
            continue

        with open(file_path, "r") as f:
            for line in f:
                match = re.match(pattern, line)
                if not match:
                    continue
                entry = match.groupdict()

                # Timestamp normalization
                ts_raw = entry["timestamp"]
                try:
                    if file_name in ["dmesg.txt", "Xorg.0.log.txt"]:
                        ts = dt.fromtimestamp(float(ts_raw), tz=datetime.timezone.utc)
                        ts = ts.replace(year=date.year, month=date.month, day=date.day)
                    else:
                        ts = dt.fromisoformat(ts_raw)
                except Exception:
                    continue

                date_key = ts.strftime("%Y-%m-%d")

                # Infer log level
                msg = entry.get("message", "")
                level_match = re.search(r"\b(INFO|ERROR|WARNING|DEBUG|CRITICAL|BLOCK|DENY|ACCEPT|FAIL|FATAL)\b", msg, re.IGNORECASE)
                log_level = level_match.group(1).upper() if level_match else "UNKNOWN"

                log_record = {
                    "timestamp": ts.isoformat(),
                    "source": file_name,
                    "log_level": log_level,
                    "message": msg
                }

                if "process" in entry:
                    log_record["process"] = entry["process"]
                if "host" in entry:
                    log_record["host"] = entry["host"]

                logs.setdefault(date_key, []).append(log_record)

    # Write to JSON
    with open(output_path, "w") as out:
        json.dump(logs, out, indent=2)

        print(f"2ND TEST CASE PASSED AND FILE CREATED:{output_path}")

