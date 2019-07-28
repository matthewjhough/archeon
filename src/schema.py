import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

from src.gql_types import CreateMessage, MessageType, SessionType, UserType
from src.model import Message
from src.pubsub import messages, pubsub

logger = logging.getLogger("schema")


# TODO: ADD PARAMETERS/RESOLVERS TO QUERIES

# TODO: ADD SESSION

# TODO: ADD USER/AUTHENTICATION LOGIN

# TODO: ADD AUTHORIZATION FOR USERS


class Query(graphene.ObjectType):
	node = graphene.relay.Node.Field()
	all_users = SQLAlchemyConnectionField(UserType)
	all_sessions = SQLAlchemyConnectionField(SessionType)
	all_messages = graphene.List(MessageType, user_id=graphene.String())

	def resolve_all_messages(self, info, user_id):
		try:
			logger.debug("fetching messages for user_id: %s", user_id)
			message_query = Message.query.filter_by(user_id=user_id)
			message_count = message_query.count()
			all_messages = message_query.all()
		except NameError:
			logger.error("Error occurred when fetching messages for user_id %s;\nError message: %s", user_id, NameError)
		else:
			logger.debug("returning %s messages...", message_count)
			return all_messages


class Mutation(graphene.ObjectType):
	create_message = CreateMessage.Field()


class Subscription(graphene.ObjectType):
	message = graphene.Field(MessageType, user_id=graphene.String())

	def resolve_message(root, info, **kwargs):
		# TODO: FILTER BASED ON USER ID & SESSION
		logger.debug('logging kwargs: %s', kwargs)

		def _resolve(message):
			current_user_id = kwargs['user_id']
			logger.info('current user id: %s', current_user_id)
			logger.info('message user_id: %s', message.user_id)
			is_current_user = str(current_user_id) == str(message.user_id)
			logger.debug("message user is current user: %s", is_current_user)
			if is_current_user:
				return message

			return

		return pubsub. \
			filter(lambda msg: msg[0] == 'message'). \
			map(lambda msg: _resolve(msg[1]))


pubsub.subscribe(messages.append)

schema = graphene.Schema(
	query=Query,
	mutation=Mutation,
	subscription=Subscription
)
