from flask import Flask, render_template, request, redirect, url_for, flash
from models import init_db, get_all_todos, get_todo, create_todo, update_todo, toggle_todo, delete_todo, get_stats

app = Flask(__name__)
app.secret_key = 'todo-plus-secret-key'

CATEGORIES = ['general', 'work', 'personal', 'study', 'health']
PRIORITIES = ['high', 'medium', 'low']


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
