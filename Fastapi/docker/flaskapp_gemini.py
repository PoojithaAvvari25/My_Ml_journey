import os
import sqlite3
from flask import Flask, flash, redirect, render_template_string, request, url_for

app = Flask(__name__)
# Secret key is required for session-based features like flashing messages
app.config["SECRET_KEY"] = os.urandom(24)
DATABASE = "tasks.db"


# --- DATABASE SETUP ---
def get_db():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like a dict
    return conn


def init_db():
    """Creates the tasks table if it does not exist yet."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0
            )
        """
        )
        conn.commit()


# --- INLINE HTML TEMPLATE ---
# Uses Tailwind CSS via CDN for clean, responsive UI styling without separate CSS files
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager (Flask Medium)</title>
    <script src="https://jsdelivr.net"></script>
</head>
<body class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-md">
        <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">📋 Flask Task Manager</h1>

        <!-- Flash Messages for feedback -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="mb-4 p-4 rounded {{ 'bg-green-100 text-green-700' if category == 'success' else 'bg-red-100 text-red-700' }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <!-- Add Task Form -->
        <form action="{{ url_for('add_task') }}" method="POST" class="mb-8 space-y-4">
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Task Title*</label>
                <input type="text" name="title" required class="w-full border p-2 rounded focus:outline-blue-500" placeholder="What needs to be done?">
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Description</label>
                <textarea name="description" class="w-full border p-2 rounded focus:outline-blue-500" placeholder="Optional details..."></textarea>
            </div>
            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition">Add Task</button>
        </form>

        <!-- Tasks List -->
        <h2 class="text-xl font-bold text-gray-700 mb-4">Your Tasks ({{ tasks|length }})</h2>
        <ul class="space-y-3">
            {% for task in tasks %}
                <li class="flex items-center justify-between p-4 border rounded-lg {{ 'bg-gray-50 line-through text-gray-400' if task.completed else 'bg-white' }}">
                    <div class="flex-1 pr-4">
                        <h3 class="font-semibold text-lg">{{ task.title }}</h3>
                        {% if task.description %}
                            <p class="text-sm text-gray-500">{{ task.description }}</p>
                        {% endif %}
                    </div>
                    <div class="flex items-center space-x-2">
                        {% if not task.completed %}
                            <a href="{{ url_for('complete_task', task_id=task.id) }}" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm font-medium">Done</a>
                        {% endif %}
                        <a href="{{ url_for('delete_task', task_id=task.id) }}" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm font-medium" onclick="return confirm('Delete this task?')">Delete</a>
                    </div>
                </li>
            {% else %}
                <p class="text-gray-500 text-center py-4">No tasks found. Add one above!</p>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


# --- ROUTES / CONTROLLERS ---


# Read operation
@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, tasks=tasks)


# Create operation with validation
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("Task title is required!", "error")
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description)
    )
    conn.commit()
    conn.close()

    flash("Task added successfully!", "success")
    return redirect(url_for("index"))


# Update operation
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = get_db()
    conn.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    flash("Task marked as completed!", "success")
    return redirect(url_for("index"))


# Delete operation
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    flash("Task deleted!", "success")
    return redirect(url_for("index"))


# --- APPLICATION ENTRY POINT ---
if __name__ == "__main__":
    init_db()  # Setup database on launch
    app.run(host="0.0.0.0",debug=True, port=5000)
