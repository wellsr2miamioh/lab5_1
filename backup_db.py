import os

def backup_file(original, backup):
    try:
        with open(original, 'rb') as src, open(backup, 'wb') as dst:
            dst.write(src.read())
        print(f"Backup successful: {backup}")
    except Exception as e:
        print(f"Error: {e}")

# Usage
original_file = '/nfs/data/demo.db'  # Source file
backup_file_path = '/nfs/data/demo_backup.db'  # Destination backup file

backup_file(original_file, backup_file_path)
