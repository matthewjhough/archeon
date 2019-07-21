import os
from flask import Flask
from model import Post, User, Message
from app import app, db


def initialize(db):
    with app.app_context():
        db.create_all()
        john = User(username='johndoe')
        post = Post()
        post.title = "Hello World"
        post.body = "This is the first post"
        post.author = john
        db.session.add(post)
        db.session.add(john)
        db.session.commit()
        User.query.all()
        Post.query.all()


initialize(db)
