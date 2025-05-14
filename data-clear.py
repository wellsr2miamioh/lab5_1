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


if __name__ == '__main__':
    clear_test_tasks()  # optional: only call if you still want this
    clear_dast_tasks()  # this is your DAST-focused cleanup
