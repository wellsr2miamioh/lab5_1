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

def generate_test_data():
    """Generate test data if not already present."""
    db = connect_db()
    if db is None:
        print("Database connection failed, unable to generate test data.")
        return

    try:
        cursor = db.cursor()  # Create a cursor object
        
        # Check if the table is empty
        cursor.execute('SELECT COUNT(*) FROM tasks')
        if cursor.fetchone()[0] == 0:  # Check if there are any rows
            test_data = [
                ('Test Task 1', 'Test Description for Task 1', 'pending'),
                ('Test Task 2', 'Test Description for Task 2', 'completed'),
                ('Test Task 3', 'Test Description for Task 3', 'pending'),
                ('Test Task 4', 'Test Description for Task 4', 'completed')
            ]
            cursor.executemany('INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)', test_data)
            db.commit()
            print("Test data generated successfully.")
        else:
            print("Test data already exists.")
        
    except sqlite3.Error as e:
        print(f"Error during database operation: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    generate_test_data()
