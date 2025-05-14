import sqlite3
from datetime import datetime, timedelta

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def clear_test_tasks():
    """Delete tasks that follow a specific naming pattern (e.g., 'Test Task %')."""
    db = connect_db()
    db.execute("DELETE FROM tasks WHERE taskName LIKE 'Test Task %'")
    db.commit()
    print('Test tasks have been deleted from the database.')
    db.close()

def clear_dast_tasks():
    """Delete unprotected tasks created recently (e.g., by DAST scans)."""
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
    # You can call either or both
    clear_test_tasks()
    clear_dast_tasks()


