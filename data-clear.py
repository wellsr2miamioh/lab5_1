import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    try:
        return sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def clear_test_tasks():
    """Clear only the test tasks from the database."""
    db = connect_db()
    if db is None:
        print("Database connection failed, unable to clear test tasks.")
        return
    
    try:
        # Assuming all test tasks follow a specific naming pattern
        db.execute("DELETE FROM tasks WHERE name LIKE 'Test Task %'")
        db.commit()
        print('Test tasks have been deleted from the database.')
    except sqlite3.Error as e:
        print(f"Error during database operation: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    clear_test_tasks()
