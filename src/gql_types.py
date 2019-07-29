import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.db import db
from src.model import Message, Session, User
from src.pubsub import messages, pubsub

logger = logging.getLogger("gql_types")
relay = graphene.relay


# Types


class UserType(SQLAlchemyObjectType):
	class Meta:
		model = User
		interfaces = (relay.Node,)


class SessionType(SQLAlchemyObjectType):
	class Meta:
		model = Session
		interfaces = (relay.Node,)


class MessageType(SQLAlchemyObjectType):
	class Meta:
		model = Message
		interfaces = (relay.Node,)


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

		user = User.query.filter_by(username=username).first()
		session = Session.query.filter(Session.uuid == session_id).first()
		message = Message(content=content)

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
