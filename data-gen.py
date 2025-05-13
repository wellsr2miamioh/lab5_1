import sqlite3
import os

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def generate_test_tasks(num_tasks):
    """Generate test data for the tasks table."""
    db = connect_db()
    for i in range(num_tasks):
        task_name = f'Test Task {i}'
        task_description = f'This is a description for task {i}'
        db.execute(
            'INSERT INTO tasks (taskName, taskDescription, completed) VALUES (?, ?, ?)',
            (task_name, task_description, 0)
        )
    db.commit()
    print(f'{num_tasks} test tasks added to the database.')
    db.close()

if __name__ == '__main__':
    generate_test_tasks(10)  # Add 10 test tasks

