from main import db
from applications.data.database import Base
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True)
    correct = db.Column(db.Integer, nullable=False, default=0)
    incorrect = db.Column(db.Integer, nullable=False, default=0)
    roles = db.relationship('Role', secondary='users_roles', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False, unique=True)

class User_Role(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), default=2)

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    question = db.Column(db.String(64), nullable=False)
    answer = db.Column(db.String(64), nullable=False)
    deck = db.Column(db.String(16), nullable=False)