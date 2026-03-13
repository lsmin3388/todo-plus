import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'todo.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT DEFAULT 'general',
            priority TEXT DEFAULT 'medium',
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def get_all_todos(category=None, priority=None, status=None):
    conn = get_db()
    query = "SELECT * FROM todos WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status == 'completed':
        query += " AND completed = 1"
    elif status == 'active':
        query += " AND completed = 0"

    query += " ORDER BY completed ASC, CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END, created_at DESC"

    todos = conn.execute(query, params).fetchall()
    conn.close()
    return todos


def get_todo(todo_id):
    conn = get_db()
    todo = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    return todo


def create_todo(title, description, category, priority, due_date):
    conn = get_db()
    conn.execute(
        "INSERT INTO todos (title, description, category, priority, due_date) VALUES (?, ?, ?, ?, ?)",
        (title, description, category, priority, due_date or None)
    )
    conn.commit()
    conn.close()


def update_todo(todo_id, title, description, category, priority, due_date):
    conn = get_db()
    conn.execute(
        "UPDATE todos SET title=?, description=?, category=?, priority=?, due_date=? WHERE id=?",
        (title, description, category, priority, due_date or None, todo_id)
    )
    conn.commit()
    conn.close()


def toggle_todo(todo_id):
    conn = get_db()
    conn.execute("UPDATE todos SET completed = NOT completed WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()


def delete_todo(todo_id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM todos WHERE completed = 1").fetchone()[0]
    active = total - completed

    categories = conn.execute(
        "SELECT category, COUNT(*) as count FROM todos GROUP BY category"
    ).fetchall()

    priorities = conn.execute(
        "SELECT priority, COUNT(*) as count FROM todos GROUP BY priority"
    ).fetchall()

    conn.close()
    return {
        'total': total,
        'completed': completed,
        'active': active,
        'completion_rate': round(completed / total * 100) if total > 0 else 0,
        'categories': {row['category']: row['count'] for row in categories},
        'priorities': {row['priority']: row['count'] for row in priorities}
    }