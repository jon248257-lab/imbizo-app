import zipfile
import os
import shutil
from datetime import datetime

DATA_DIR = "data"
BACKUP_DIR = "data/backups"

class Backup:
    @staticmethod
    def create_backup():
        os.makedirs(BACKUP_DIR, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
        backup_file = f"{BACKUP_DIR}/backup_{date_str}.zip"

        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(DATA_DIR):
                for file in files:
                    if not file.endswith('.zip'): # don't backup backups inside backup
                        zipf.write(os.path.join(root, file))
        return backup_file

    @staticmethod
    def restore_backup(zip_path):
        try:
            shutil.rmtree(DATA_DIR) # delete old data
            os.makedirs(DATA_DIR)
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(".")
            return True, "Restore complete. Restart app."
        except Exception as e:
            return False, f"Restore failed: {e}"
