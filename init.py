from model import User
from app import app, db


def initialize(db):
    with app.app_context():
        db.create_all()
        john = User(username='johndoe')
        db.session.add(john)
        db.session.commit()
        User.query.all()


initialize(db)
