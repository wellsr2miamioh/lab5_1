import shutil

backup = '/nfs/demo_backup.db'
original = '/nfs/demo.db'

shutil.copyfile(backup, original)
print("Database restored.")
