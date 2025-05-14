import sqlite3
from datetime import datetime, timedelta

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def clear_test_tasks():
    db = connect_db()
    db.execute("DELETE FROM tasks WHERE taskName LIKE 'Test Task %'")
    db.commit()
    print('Test tasks have been deleted from the database.')
    db.close()

def clear_dast_tasks():
    db = connect_db()
    cursor = db.cursor()

    cutoff = datetime.utcnow() - timedelta(minutes=10)
    cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        DELETE FROM tasks
        WHERE protected = 0 AND created_at >= ?
    """, (cutoff_str,))
    db.commit()
    print(f"DAST cleanup: Deleted unprotected tasks created after {cutoff_str}")
    db.close()

if __name__ == '__main__':
    clear_test_tasks()  # optional: only call if you still want this
    clear_dast_tasks()  # this is your DAST-focused cleanup
