import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

from src.gql_types import CreateMessage, MessageType, SessionType, UserType
from src.model import Message, User
from src.pubsub import messages, pubsub

logger = logging.getLogger("schema")


# TODO: ADD PARAMETERS/RESOLVERS TO QUERIES

# TODO: ADD SESSION

# TODO: ADD USER/AUTHENTICATION LOGIN

# TODO: ADD AUTHORIZATION FOR USERS


class Query(graphene.ObjectType):
	node = graphene.relay.Node.Field()
	user = graphene.Field(lambda: UserType, user_id=graphene.String())
	users = SQLAlchemyConnectionField(UserType)
	sessions = graphene.List(lambda: SessionType)
	messages = graphene.List(MessageType, user_id=graphene.String())

	def resolve_user(self, info, user_id):
		logger.info("getting user, with id %s", user_id)
		user = User.query.filter(User.uuid == user_id).first()
		logger.info("returning user: %s", user)
		return user

	def resolve_sessions(self, info):
		query = SessionType.get_query(info)
		session_count = query.count()
		all_sessions = query.all()
		logger.debug("returning %s sessions...", session_count)
		return all_sessions

	def resolve_messages(self, info, user_id):
		# TODO: CHECK USER_ID + SESSION_ID TO RETURN MESSAGES IN SESSION
		logger.debug("fetching messages for user_id: %s", user_id)
		message_query = Message.query.filter_by(user_id=user_id)
		message_count = message_query.count()
		all_messages = message_query.all()
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
