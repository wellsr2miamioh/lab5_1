import sqlite3
from datetime import datetime
import os

DATABASE = '/nfs/demo.db'
BACKUP_DIR = '/nfs/backups'
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_db():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"demo_backup_{timestamp}.db")

        # Backup using SQLite's built-in backup method
        src = sqlite3.connect(DATABASE)
        dst = sqlite3.connect(backup_path)
        with dst:
            src.backup(dst)
        src.close()
        dst.close()

        print(f"Database backed up to {backup_path}")
        return backup_path

    except Exception as e:
        print(f"Error during backup: {e}")
        return None

if __name__ == "__main__":
    backup_db()
