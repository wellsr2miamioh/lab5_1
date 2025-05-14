import shutil

original = '/nfs/data/demo.db'
backup = '/nfs/data/demo_backup.db'

shutil.copyfile(original, backup)
print("Database backed up.")
