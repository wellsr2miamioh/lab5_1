from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Enables dict-like access to rows
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('DROP TABLE IF EXISTS tasks')  # <-- force table rebuild
        db.execute('''
            CREATE TABLE tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                taskName TEXT NOT NULL,
                taskDescription TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            );
        ''')
        db.commit()
        
@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Feedback message

    if request.method == 'POST':
        action = request.form.get('action')
        task_id = request.form.get('task_id')

        if action == 'delete':
            db = get_db()
            db.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
            db.commit()
            message = 'Task deleted successfully.'

        elif action == 'complete':
            db = get_db()
            db.execute('UPDATE tasks SET completed = 1 WHERE task_id = ?', (task_id,))
            db.commit()
            message = 'Task marked as completed.'

        else:
            taskName = request.form.get('taskName')
            taskDescription = request.form.get('taskDescription')
            if taskName and taskDescription:
                db = get_db()
                db.execute('INSERT INTO tasks (taskName, taskDescription) VALUES (?, ?)', (taskName, taskDescription))
                db.commit()
                message = 'Task added successfully.'
            else:
                message = 'Missing task name or description.'

    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()



    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Task List</title>
            <style>
            body {background-color: powderblue; font-family:Arial;}
            h1   {color: blue;}
            </style>
            
        </head>
        <body>
            <h2>To-Do List</h2>
            <form method="POST" action="/">
                <label for="taskName">Task Name:</label><br>
                <input type="text" id="taskName" name="taskName" required><br>
                <label for="taskDescription">Task Description:</label><br>
                <input type="text" id="taskDescription" name="taskDescription"><br><br>
                <input type="submit" value="Submit">
            </form>

            <p>{{ message }}</p>

            {% if tasks %}
                <table border="1">
                    <tr>
                        <th>Task Name</th>
                        <th>Task Description</th>
                        <th>Mark Complete</th>
                        <th>Delete</th>
                    </tr>
                    {% for task in tasks %}
                        <tr style="color: {% if task['completed'] %}gray{% else %}black{% endif %};">
                            <td>{{ task['taskName'] }}</td>
                            <td>{{ task['taskDescription'] }}</td>
                            <td>
                                {% if task['completed'] == 0 %}
                                    <form method="POST" action="/">
                                        <input type="hidden" name="task_id" value="{{ task['task_id'] }}">
                                        <input type="hidden" name="action" value="complete">
                                        <input type="submit" value="Mark Completed">
                                    </form>
                                {% else %}
                                    ✅ Completed
                                {% endif %}
                            </td>
                            <td>
                                <form method="POST" action="/">
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

    @app.route('/cleanup-dastardly-tasks', methods=['POST'])
def cleanup_dastardly_tasks():
    db = get_db()
    db.execute("""
        DELETE FROM tasks 
        WHERE taskDescription = 'SMNcQy'
        AND (
            taskName LIKE '%<%' OR
            taskName LIKE '%>%'
            OR taskName LIKE '%alert%' 
            OR taskName LIKE '%a%' 
            OR taskName LIKE '%&#%' 
            OR taskName LIKE '%/%' 
            OR taskName LIKE '%"%'
            OR taskName LIKE '%=%'
        )
    """)
    db.commit()
    return "DAST test tasks cleaned up.", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)

