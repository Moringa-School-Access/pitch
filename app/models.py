from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    photos = db.relationship('PhotoProfile', backref='user', lazy="dynamic")
    # password_secure = db.Column(db.String(255))

    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'
    id = db.Column(db.Integer, primary_key=True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


# class FormInput(db.Model):
#     __table__ = 'pitch'
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
