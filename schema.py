import graphene
import random
from rx import Observable
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
# from graphql_ws.pubsub import GeventRxRedisPubsub
from model import Post, User, Message
from db import db

# TODO: SETUP PUBSUB FOR SUBSCRIPTIONS / MUTATIONS.

# TODO: ADD PARAMETERS/RESOLVERS TO QUERIES

# TODO: ADD USER/AUTHENTICATION LOGIN

# TODO: ADD AUTHORIZATION FOR USERS
# pubsub = GeventRxRedisPubsub()

# Types


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )


class PostType(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )


class MessageType(SQLAlchemyObjectType):
    class Meta:
        model = Message
        interfaces = (graphene.relay.Node, )


# example subscription class


class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


# Mutations
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        username = graphene.String(required=True)
    post = graphene.Field(lambda: PostType)

    def mutate(self, info, title, body, username):

        user = User.query.filter_by(username=username).first()
        post = Post(title=title, body=body)

        if user is not None:
            post.author = user

        db.session.add(post)
        db.session.commit()

        return CreatePost(post=post)


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

        if Subscription is not None:
            Subscription.resolve_message_added(Subscription, message)

        db.session.add(message)
        db.session.commit()
        return CreateMessage(message=message)


# Combine schemas
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostType)
    all_users = SQLAlchemyConnectionField(UserType)
    all_messages = SQLAlchemyConnectionField(MessageType)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_message = CreateMessage.Field()


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())

    random_int = graphene.Field(RandomType)

    message_added = graphene.Field(lambda: MessageType)

    def resolve_message_added(root, info):
        print("*** resolve message ***")
        print(info)
        print(root)

        message = db.session.query(Message).order_by(
            Message.uuid.desc()).first()

        messageStream = Observable.of(message)

        if hasattr(info, "uuid"):
            print("Message created, publishing message...")
            return messageStream

        print("publishing...")
        return messageStream

    def resolve_count_seconds(root, info, up_to=5):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

    def resolve_random_int(root, info):
        return Observable.interval(1000).map(lambda i: RandomType(seconds=i, random_int=random.randint(0, 500)))


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
