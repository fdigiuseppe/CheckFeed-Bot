#!/usr/bin/env python3
"""
Script di test per verificare la funzione cleanup_logs
"""
import sys
import os
sys.path.append('.')

from bot.logger import cleanup_logs
from bot.config_loader import get_config

# Carica la configurazione
config = get_config()
retention_days = config.get("data_retention_days", 7)

print(f"🧹 Eseguendo cleanup con retention di {retention_days} giorni...")

# Lista i file prima del cleanup
log_dir = "data/logs"
if os.path.exists(log_dir):
    files_before = os.listdir(log_dir)
    print(f"📁 File di log prima del cleanup: {len(files_before)}")
    for f in sorted(files_before):
        print(f"   - {f}")
else:
    print("📁 Cartella logs non trovata")

# Esegui il cleanup
try:
    cleanup_logs(retention_days)
    print("✅ Cleanup eseguito con successo")
except Exception as e:
    print(f"❌ Errore durante cleanup: {e}")
    import traceback
    traceback.print_exc()

# Lista i file dopo il cleanup
if os.path.exists(log_dir):
    files_after = os.listdir(log_dir)
    print(f"📁 File di log dopo il cleanup: {len(files_after)}")
    for f in sorted(files_after):
        print(f"   - {f}")