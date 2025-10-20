import os
from datetime import timedelta, datetime

LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log(message: str):
    """Scrive un messaggio su console e sul file di log giornaliero."""
    now = datetime.now()
    log_file = os.path.join(LOG_DIR, f"{now.date()}.log")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")
    print(message)

def cleanup_logs(retention_days: int):
    """Elimina i file di log più vecchi di retention_days."""
    cutoff_date = datetime.now().date() - timedelta(days=retention_days)
    for file in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, file)
        if os.path.isfile(path) and file.endswith(".log"):
            file_date_str = file.replace(".log", "")
            try:
                # Parse della data del file (formato YYYY-MM-DD)
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
                if file_date < cutoff_date:
                    os.remove(path)
                    log(f"🗑️ Rimosso log vecchio: {file}")
            except Exception as e:
                continue

