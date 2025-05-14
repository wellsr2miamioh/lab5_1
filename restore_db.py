import os

def restore_file(backup, original):
    try:
        with open(backup, 'rb') as src, open(original, 'wb') as dst:
            dst.write(src.read())
        print(f"Restore successful: {original}")
    except Exception as e:
        print(f"Error: {e}")

# Usage
backup_file_path = '/nfs/data/demo_backup.db'  # Source backup file
original_file = '/nfs/data/demo.db'  # Destination (original) file

restore_file(backup_file_path, original_file)
