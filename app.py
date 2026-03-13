from flask import Flask, render_template, request, redirect, url_for, flash
from models import init_db, get_all_todos, get_todo, create_todo, update_todo, toggle_todo, delete_todo, get_stats

app = Flask(__name__)
app.secret_key = 'todo-plus-secret-key'

CATEGORIES = ['general', 'work', 'personal', 'study', 'health']
PRIORITIES = ['high', 'medium', 'low']


@app.route('/')
def index():
    category = request.args.get('category')
    priority = request.args.get('priority')
    status = request.args.get('status')
    todos = get_all_todos(category=category, priority=priority, status=status)
    return render_template('index.html', todos=todos, categories=CATEGORIES,
                           priorities=PRIORITIES, current_category=category,
                           current_priority=priority, current_status=status)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('add'))

        create_todo(
            title=title,
            description=request.form.get('description', '').strip(),
            category=request.form.get('category', 'general'),
            priority=request.form.get('priority', 'medium'),
            due_date=request.form.get('due_date', '')
        )
        flash('Todo added successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', todo=None, categories=CATEGORIES, priorities=PRIORITIES)


@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = get_todo(todo_id)
    if not todo:
        flash('Todo not found.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return redirect(url_for('edit', todo_id=todo_id))

        update_todo(
            todo_id=todo_id,
            title=title,
            description=request.form.get('description', '').strip(),
            category=request.form.get('category', 'general'),
            priority=request.form.get('priority', 'medium'),
            due_date=request.form.get('due_date', '')
        )
        flash('Todo updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', todo=todo, categories=CATEGORIES, priorities=PRIORITIES)


@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    toggle_todo(todo_id)
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    delete_todo(todo_id)
    flash('Todo deleted.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
