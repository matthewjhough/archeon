import logging

from app import app, db
from src.model import Session, User

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

		# commit / flush
		db.session.commit()
		db.session.flush()
		# end commit / flush

		logger.info("db flushed, data saved.")

		logger.info("user %s added", test2.username)
		chat_session = Session()

		# commit / flush
		db.session.commit()
		db.session.flush()
		# end commit / flush

		# chat_session.users.add(test)
		# chat_session.users.add(test2)
		chat_session.users = [test, test2]

		db.session.add(chat_session)

		# commit / flush
		db.session.commit()
		db.session.flush()
		# end commit / flush

		logger.info("initialization complete.")


initialize(db)
