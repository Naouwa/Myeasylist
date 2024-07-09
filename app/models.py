# app/models.py

from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='To Do')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignees = db.relationship('User', secondary='task_assignees', backref=db.backref('assigned_tasks', lazy='dynamic'))

    def __repr__(self):
        return f"Task('{self.title}', '{self.due_date}', '{self.status}')"

# Define Task Assignees association table
task_assignees = db.Table('task_assignees',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
