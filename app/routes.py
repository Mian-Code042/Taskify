from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import db, Todo, User
from datetime import datetime
import re

main = Blueprint('main', __name__)

# Import the limiter from __init__
from app import limiter

@main.route('/')
@login_required
def index():
    # Fetch user specific todos
    todo_list = Todo.query.filter_by(user_id=current_user.id).all()
    # Until we have the new index.html ready, we just return a stub so it doesn't crash on the old template
    return render_template('index.html', todo_list=todo_list)

@main.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute") # Rate limit login attempts
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

def is_password_strong_enough(password):
    """Check if password meets minimum complexity requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    return True, ""

@main.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute") # Rate limit registration attempts
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('main.register'))
            
        # Password validation
        is_valid, msg = is_password_strong_enough(password)
        if not is_valid:
            flash(msg, 'danger')
            return redirect(url_for('main.register'))
            
        new_user = User(
            username=username, 
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    priority = request.form.get('priority', 'Medium')
    due_date_str = request.form.get('due_date')
    
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('main.index'))

    if title:
        new_todo = Todo(
            title=title, 
            user_id=current_user.id,
            priority=priority,
            due_date=due_date
        )
        db.session.add(new_todo)
        db.session.commit()
        flash('Task added!', 'success')
    else:
        flash('Task title is required.', 'danger')
        
    return redirect(url_for('main.index'))

@main.route('/update/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    if todo.user_id != current_user.id:
        flash('Unauthorized to edit this task.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.status = request.form.get('status')
        todo.priority = request.form.get('priority')
        
        due_date_str = request.form.get('due_date')
        if due_date_str:
            try:
                todo.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.', 'danger')
        else:
            todo.due_date = None
            
        todo.complete = (todo.status == 'Completed')
        
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('edit.html', todo=todo)

@main.route('/delete/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
        flash('Task deleted.', 'info')
    else:
        flash('Unauthorized to delete this task.', 'danger')
        
    return redirect(url_for('main.index'))

@main.route('/toggle/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def toggle(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id == current_user.id:
        todo.complete = not todo.complete
        todo.status = 'Completed' if todo.complete else 'Pending'
        db.session.commit()
    return redirect(url_for('main.index'))
