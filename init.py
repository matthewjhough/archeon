import logging
from src.model import User
from app import app, db

logger = logging.getLogger("initialization")


# TODO: SEND AJAX REQUEST TO ENDPOINT FOR CONFIG FILE DATA, THEN WRITE FILES IN /config DIR


def initialize(db):
	with app.app_context():
		logger.info("initializing db..")

		db.create_all()
 
		test = User(username='test')
		db.session.add(test)
		db.session.commit()

		logger.info("user %s added", test.username)

		User.query.all()

		test2 = User(username='test2')
		db.session.add(test2)
		db.session.commit()

		logger.info("user %s added", test2.username)

		logger.info("initialization complete.")


initialize(db)
