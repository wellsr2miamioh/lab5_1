from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                taskName TEXT NOT NULL,
                taskDescription TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                protected INTEGER DEFAULT 1
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''

    if request.method == 'POST':
        action = request.form.get('action')
        task_id = request.form.get('task_id')

        if action == 'delete':
            db = get_db()
            db.execute('DELETE FROM tasks WHERE task_id = ? AND protected = 0', (task_id,))
            db.commit()
            message = 'Task deleted (if not protected).'

        elif action == 'complete':
            db = get_db()
            db.execute('UPDATE tasks SET completed = 1 WHERE task_id = ?', (task_id,))
            db.commit()
            message = 'Task marked as completed.'

        else:
            taskName = request.form.get('ta


