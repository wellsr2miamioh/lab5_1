from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute(''' 
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            task_id = request.form.get('task_id')
            db = get_db()
            db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            db.commit()
            message = 'Task deleted successfully.'
        # Check if it's a mark completed action
        elif request.form.get('action') == 'complete':
            task_id = request.form.get('task_id')
            db = get_db()
            db.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_id,))
            db.commit()
            message = 'Task marked as completed.'
        else:
            name = request.form.get('name')
            description = request.form.get('description')
            if name and description:
                db = get_db()
                db.execute('INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)', (name, description, 'pending'))
                db.commit()
                message = 'Task added successfully.'
            else:
                message = 'Missing name or description.'

    # Always display the tasks table
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()

    # Display the HTML form along with the tasks table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tasks</title>
        </head>
        <body>
            <h2>Add Task</h2>
            <form method="POST" action="/">
                <label for="name">Task Name:</label><br>
                <input type="text" id="name" name="name" required><br>
                <label for="description">Description:</label><br>
                <input type="text" id="description" name="description" required><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>{{ message }}</p>
            {% if tasks %}
                <table border="1">
                    <tr>
                        <th>Task Name</th>
                        <th>Description</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                    {% for task in tasks %}
                        <tr>
                            <td>{{ task['name'] }}</td>
                            <td>{{ task['description'] }}</td>
                            <td>{{ task['status'] }}</td>
                            <td>
                                {% if task['status'] == 'pending' %}
                                    <form method="POST" action="/">
                                        <input type="hidden" name="task_id" value="{{ task['id'] }}">
                                        <input type="hidden" name="action" value="complete">
                                        <input type="submit" value="Mark as Completed">
                                    </form>
                                {% endif %}
                                <form method="POST" action="/">
                                    <input type="hidden" name="task_id" value="{{ task['id'] }}">
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
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)

