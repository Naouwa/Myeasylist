from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db, bcrypt
from app.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import or_

@app.route("/")
@app.route("/home")
@login_required
def home():
    tasks = Task.query.filter(or_(Task.author == current_user, Task.assignees.any(User.id == current_user.id)))
    return render_template('home.html', tasks=tasks)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title')
        due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
        task = Task(title=title, due_date=due_date, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_task.html')

@app.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
        task.status = request.form.get('status')
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template('update_task.html', task=task)

@app.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/task/<int:task_id>/update_status", methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    data = request.get_json()
    new_status = data.get('status')
    task.status = new_status
    db.session.commit()
    return jsonify({'success': True})
