import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def clear_dast_tasks():
    """
    Delete all unprotected tasks.
    """
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE protected = 0
    """)
    deleted = cursor.rowcount
    db.commit()
    db.close()
    print(f"DAST cleanup: removed {deleted} unprotected tasks.")

if __name__ == '__main__':
    clear_dast_tasks()
