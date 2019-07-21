import graphene
import random
from rx import Observable
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from model import Post, User, Message, RandomType
from db import db


# Types


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )


class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )


class MessageObject(SQLAlchemyObjectType):
    class Meta:
        model = Message
        interfaces = (graphene.relay.Node, )


# Mutations
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        username = graphene.String(required=True)
    post = graphene.Field(lambda: PostObject)

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
    message = graphene.Field(lambda: MessageObject)

    def mutate(self, info, content, username):
        user = User.query.filter_by(username=username).first()
        message = Message(content=content)
        if user is not None:
            message.user = user
        db.session.add(message)
        db.session.commit()
        return CreateMessage(message=message)


# Combine schemas
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)
    all_messages = SQLAlchemyConnectionField(MessageObject)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_message = CreateMessage.Field()


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())

    random_int = graphene.Field(RandomType)

    messages = SQLAlchemyConnectionField(
        MessageObject
    )

    def resolve_messages(self, args, context, info):
        print("Info: " + info)
        query = Message.get_query(context)
        return query.filter_by(uuid=info.root_value.get('uuid'))

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
