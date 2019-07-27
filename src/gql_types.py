import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.db import db
from src.model import Message, User
from src.pubsub import messages, pubsub

logger = logging.getLogger("gql_types")


# Types
 

class UserType(SQLAlchemyObjectType):
	class Meta:
		model = User
		interfaces = (graphene.relay.Node,)


class MessageType(SQLAlchemyObjectType):
	class Meta:
		model = Message
		interfaces = (graphene.relay.Node,)


class CreateMessage(graphene.Mutation):
	class Arguments:
		content = graphene.String(required=True)
		username = graphene.String(required=True)

	message = graphene.Field(lambda: MessageType)

	def mutate(self, info, content, username):
		logger.info("username: %s submitting message content: %s", username, content)

		user = User.query.filter_by(username=username).first()
		message = Message(content=content)

		if user is not None:
			logger.info("user found, assigning user to message.")
			message.user = user

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
