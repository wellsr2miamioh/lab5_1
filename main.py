from flask import Flask, request, render_template_string
import sqlite3
import os
from datetime import datetime

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
            CREATE TABLE IF NOT EXISTS tasksList (
                task_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                taskName     TEXT    NOT NULL,
                taskDescription TEXT NOT NULL,
                completed    INTEGER DEFAULT 0,
                created_at   TEXT    DEFAULT CURRENT_TIMESTAMP,
                protected    INTEGER DEFAULT 1
            );
        ''')

        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''

    if request.method == 'POST':
        action    = request.form.get('action')
        task_id   = request.form.get('task_id')

        if action == 'delete' and task_id:
            # DELETE ignores protected flag entirely
            db = get_db()
            db.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
            db.commit()
            message = 'Task deleted successfully.'

        elif action == 'complete' and task_id:
            db = get_db()
            db.execute('UPDATE tasks SET completed = 1 WHERE task_id = ?', (task_id,))
            db.commit()
            message = 'Task marked as completed.'

        else:
            taskName        = request.form.get('taskName')
            taskDescription = request.form.get('taskDescription')
            if taskName and taskDescription:
                db = get_db()
                # Explicitly set created_at so it never ends up blank
                db.execute('''
                    INSERT INTO tasks
                      (taskName, taskDescription, created_at, protected)
                    VALUES (?, ?, datetime('now'), 1)
                ''', (taskName, taskDescription))
                db.commit()
                message = 'Task added successfully.'
            else:
                message = 'Missing task name or description.'


    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Task List</title>
            <style>
                body { background-color: powderblue; font-family: Arial; }
                h2   { color: blue; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #444; padding: 8px; text-align: left; }
            </style>
        </head>
        <body>
            <h2>To-Do List</h2>
            <form method="POST" action="/">
                <label>Task Name:</label><br>
                <input type="text" name="taskName" required><br>
                <label>Task Description:</label><br>
                <input type="text" name="taskDescription"><br><br>
                <input type="submit" value="Add Task">
            </form>

            <p>{{ message }}</p>

            {% if tasks %}
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Created At</th>
                        <th>Completed</th>
                        <th>Actions</th>
                    </tr>
                    {% for task in tasks %}
                        <tr style="color: {% if task['completed'] %}gray{% else %}black{% endif %};">
                            <td>{{ task['taskName'] }}</td>
                            <td>{{ task['taskDescription'] }}</td>
                            <td>{{ task['created_at'] }}</td>
                            <td>{% if task['completed'] %}✅{% else %}—{% endif %}</td>
                            <td>
                                {% if not task['completed'] %}
                                    <form style="display:inline" method="POST">
                                        <input type="hidden" name="task_id" value="{{ task['task_id'] }}">
                                        <input type="hidden" name="action" value="complete">
                                        <input type="submit" value="Complete">
                                    </form>
                                {% endif %}
                                <form style="display:inline" method="POST">
                                    <input type="hidden" name="task_id" value="{{ task['task_id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No tasks found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, tasks=tasks)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)


