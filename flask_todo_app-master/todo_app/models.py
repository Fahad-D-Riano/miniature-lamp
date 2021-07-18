from flask_sqlalchemy import SQLAlchemy
from todo_app import app
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def get_id(self):
        return str(self.id).encode(encoding='utf-8').decode('utf-8')


class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(80), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


db.create_all()
db.session.commit()