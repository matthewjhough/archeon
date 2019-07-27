import graphene
import logging
from graphene_sqlalchemy import SQLAlchemyConnectionField
from model import Message
from gql_types import UserType, MessageType, CreateMessage
from pubsub import pubsub, messages

logger = logging.getLogger("schema")

# TODO: ADD PARAMETERS/RESOLVERS TO QUERIES

# TODO: ADD SESSION

# TODO: ADD USER/AUTHENTICATION LOGIN

# TODO: ADD AUTHORIZATION FOR USERS


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)
    all_messages = graphene.relay.node.Field(MessageType, user_id=graphene.String())

    def resolve_all_messages(self, info, user_id):

        try:
            logger.info("fetching messages for user_id: %s", user_id)
            all_messages = Message.query.filter_by(user_id=user_id)
        except NameError:
            logger.error("Error occurred when fetching messages for user_id %s;\nError message: %s", user_id, NameError)
        else:
            logger.info("returning messages...")
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
            logger.info('message info: %s', message.user_id)
            return message

        return pubsub.\
            filter(lambda msg: msg[0] == 'message').\
            map(lambda msg: _resolve(msg[1]))


pubsub.subscribe(messages.append)

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
