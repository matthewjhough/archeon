import graphene
import random
import rx
# from rx import Observable, subjects.subjects.Subject
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from model import User, Message
from db import db

# TODO: ADD PARAMETERS/RESOLVERS TO QUERIES

# TODO: ADD USER/AUTHENTICATION LOGIN

# TODO: ADD AUTHORIZATION FOR USERS

Observable = rx.Observable
pubsub = rx.subjects.Subject()
messages = []

# Types


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )


class MessageType(SQLAlchemyObjectType):
    class Meta:
        model = Message
        interfaces = (graphene.relay.Node, )


class CreateMessage(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        username = graphene.String(required=True)
    message = graphene.Field(lambda: MessageType)

    def mutate(self, info, content, username):

        user = User.query.filter_by(username=username).first()
        message = Message(content=content)

        if user is not None:
            message.user = user

        # TODO: REPLACE WITH HTTP REQUEST TO MESSAGE SERVER
        db.session.add(message)
        db.session.commit()
        db.session.flush()

        if pubsub is not None:
            messages.append(message)
            pubsub.on_next(('message', message))


        return CreateMessage(message=message)


# Combine schemas
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserType)
    all_messages = SQLAlchemyConnectionField(MessageType)


class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()


class Subscription(graphene.ObjectType):

    message = graphene.Field(MessageType, user_id=graphene.String())

    def resolve_message(root, info, **kwargs):
        # TODO: FILTER BASED ON USER ID & SESSION
        print('(resolve_message) logging kwargs...')
        print(kwargs)

        def _resolve(message):
            current_user_id = kwargs['user_id']
            print('(resolve_message, _resolve) current user id: ' + current_user_id)
            print('(resolve_message, _resolve) mesage info: ')
            print(message.user_id)
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
