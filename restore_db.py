import sqlite3
import os
import shutil

DATABASE = '/nfs/demo.db'
BACKUP_DIR = '/nfs/backups'

# Get the latest backup file from the backup directory
def get_latest_backup():
    try:
        backup_files = os.listdir(BACKUP_DIR)
        backup_files = [f for f in backup_files if f.endswith('.db')]
        backup_files.sort(reverse=True)  # Sort to get the most recent backup
        if backup_files:
            return os.path.join(BACKUP_DIR, backup_files[0])
        else:
            print("No backup files found.")
            return None
    except Exception as e:
        print(f"Error during backup file retrieval: {e}")
        return None

def restore_db():
    try:
        latest_backup = get_latest_backup()
        if latest_backup:
            # Restore the backup into the original database
            shutil.copy(latest_backup, DATABASE)
            print(f"Database restored from {latest_backup}")
        else:
            print("No backup to restore from.")
    except Exception as e:
        print(f"Error during restore: {e}")

if __name__ == "__main__":
    restore_db()
