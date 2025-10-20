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
    deleted_count = 0
    archived_count = 0
    skipped_count = 0
    
    # Crea cartella di archivio se non esiste
    archive_dir = os.path.join(LOG_DIR, "archived")
    os.makedirs(archive_dir, exist_ok=True)
    
    print(f"DEBUG: Cutoff date = {cutoff_date}")
    print(f"DEBUG: Oggi = {datetime.now().date()}")
    
    for file in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, file)
        if os.path.isfile(path) and file.endswith(".log"):
            file_date_str = file.replace(".log", "")
            try:
                # Parse della data del file (formato YYYY-MM-DD)
                file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
                should_delete = file_date < cutoff_date
                print(f"DEBUG: {file} -> date={file_date}, should_delete={should_delete}")
                
                if should_delete:
                    try:
                        # Strategia 1: Prova cancellazione diretta
                        os.remove(path)
                        print(f"🗑️ Cancellato log vecchio: {file}")
                        print(f"DEBUG: ✅ CANCELLATO {file}")
                        deleted_count += 1
                    except (PermissionError, OSError):
                        try:
                            # Strategia 2: Sposta in archivio invece di cancellare
                            archive_path = os.path.join(archive_dir, file)
                            if os.path.exists(archive_path):
                                os.remove(archive_path)  # Rimuovi eventuale file esistente
                            os.rename(path, archive_path)
                            print(f"� Archiviato log vecchio: {file}")
                            print(f"DEBUG: ✅ ARCHIVIATO {file}")
                            archived_count += 1
                        except:
                            print(f"⚠️ File {file} completamente inaccessibile")
                            print(f"DEBUG: ⚠️ SALTATO {file} (inaccessibile)")
                            skipped_count += 1
                    except Exception as delete_error:
                        print(f"❌ Errore con {file}: {delete_error}")
                        print(f"DEBUG: ❌ ERRORE {file}: {delete_error}")
                        skipped_count += 1
                else:
                    print(f"DEBUG: ⏭️ MANTENUTO {file}")
            except Exception as e:
                print(f"DEBUG: ❌ ERRORE PARSING {file}: {e}")
                continue
    
    # Ora prova a svuotare l'archivio (file che dovrebbero essere davvero cancellati)
    archived_deleted = 0
    try:
        for archived_file in os.listdir(archive_dir):
            archived_path = os.path.join(archive_dir, archived_file)
            if archived_file.endswith(".log"):
                try:
                    os.remove(archived_path)
                    archived_deleted += 1
                    print(f"DEBUG: ✅ Cancellato dall'archivio: {archived_file}")
                except:
                    print(f"DEBUG: ⚠️ File archiviato {archived_file} ancora bloccato")
    except:
        pass
    
    total_cleaned = deleted_count + archived_deleted
    print(f"DEBUG: Risultato finale - cancellati: {total_cleaned}, archiviati: {archived_count-archived_deleted}, saltati: {skipped_count}")
    if total_cleaned > 0 or archived_count > 0 or skipped_count > 0:
        print(f"🧹 Cleanup completato: {total_cleaned} cancellati, {archived_count-archived_deleted} archiviati, {skipped_count} saltati")

