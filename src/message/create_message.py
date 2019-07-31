import logging

import graphene

from src.common.db import db
from src.common.pubsub import messages, pubsub
from src.message.message_model import MessageModel
from src.message.message_type import MessageType
from src.session.session_model import SessionModel
from src.user.user_model import UserModel

logger = logging.getLogger("create_message")


# Mutations

# TODO: IMPLMEMENT 'CREATESESSION' MUTATION TYPE

class CreateMessage(graphene.Mutation):
	class Arguments:
		content = graphene.String(required=True)
		username = graphene.String(required=True)
		session_id = graphene.String(required=True)

	message = graphene.Field(lambda: MessageType)

	# TODO: ADD SESSION_ID TO PARAMS, AND ASSIGN TO MESSAGE
	def mutate(self, info, content, username, session_id):
		logger.info("username: %s submitting message content: %s", username, content)

		user = UserModel.query.filter_by(username=username).first()
		session = SessionModel.query.filter(SessionModel.uuid == session_id).first()
		message = MessageModel(content=content)

		if user is not None:
			logger.info("user found, assigning user to message.")
			message.user = user

		if session is not None:
			logger.info("session found, assigning session to message")
			message.session = session

		# TODO: REPLACE WITH HTTP REQUEST TO MESSAGE SERVER
		db.session.add(message)
		logger.debug("adding user to session...")
		db.session.commit()
		logger.debug("committing session...")
		db.session.flush()
		logger.debug("flushing session...")

		if pubsub is not None:
			messages.append(message)
			logger.info("publishing message: %s", message)
			pubsub.on_next(('message', message))

		logger.debug("completing create message...")
		return CreateMessage(message=message)
