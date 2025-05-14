import shutil

original = '/nfs/demo.db'
backup = '/nfs/demo_backup.db'

shutil.copyfile(original, backup)
print("Database backed up.")
