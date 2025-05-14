import shutil

backup = '/nfs/data/demo_backup.db'
original = '/nfs/data/demo.db'

shutil.copyfile(backup, original)
print("Database restored.")
