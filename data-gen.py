
import sqlite3

DATABASE = '/nfs/demo.db'  # Your database location

def generate_test_data():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    # Check if the table is empty
    db.execute('SELECT COUNT(*) FROM tasks')
    if db.fetchone()[0] == 0:
        test_data = [
            ('Test Task 1', 'Test Description for Task 1', 'pending'),
            ('Test Task 2', 'Test Description for Task 2', 'completed'),
            ('Test Task 3', 'Test Description for Task 3', 'pending'),
            ('Test Task 4', 'Test Description for Task 4', 'completed')
        ]
        db.executemany('INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)', test_data)
        db.commit()
        print("Test data generated successfully.")
    else:
        print("Test data already exists.")

if __name__ == "__main__":
    generate_test_data()
