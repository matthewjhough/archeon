import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

from src.common.pubsub import messages, pubsub
from src.message.create_message import CreateMessage
from src.message.message_resolver import resolve_messages
from src.message.message_type import MessageType
from src.session.session_resolver import resolve_sessions
from src.session.session_type import SessionType
from src.user.user_resolver import resolve_user
from src.user.user_type import UserType

logger = logging.getLogger("schema")


# TODO: ADD USER/AUTHENTICATION LOGIN

# TODO: ADD AUTHORIZATION FOR USERS


class Query(graphene.ObjectType):
	node = graphene.relay.Node.Field()
	user = graphene.Field(lambda: UserType, user_id=graphene.String())
	users = SQLAlchemyConnectionField(UserType)
	sessions = graphene.List(lambda: SessionType)
	messages = graphene.List(MessageType, user_id=graphene.String())

	resolve_sessions = resolve_sessions
	resolve_user = resolve_user
	resolve_messages = resolve_messages


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
