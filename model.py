import graphene
from db import db

# Models


class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    posts = db.relationship('Post', backref='author')
    messages = db.relationship('Message', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.uuid'))

    def __repr__(self):
        return '<Post %r>' % self.title


class Message(db.Model):
    __tablename__ = 'messages'
    uuid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, index=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.uuid'))

    def __repr__(self):
        return '<Message %r>' % self.content
