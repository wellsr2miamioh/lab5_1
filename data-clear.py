import sqlite3

# Database file path, ensure this matches your Flask app
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_tasks():
    """Delete only the test tasks from the database."""
    db = connect_db()
    db.execute("DELETE FROM tasks WHERE taskName LIKE 'Test Task %'")
    db.commit()
    print('Test tasks have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_tasks()
