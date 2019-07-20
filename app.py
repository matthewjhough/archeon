
from flask import Flask
from flask_sockets import Sockets
import graphene
import os
import random
from graphql_ws.gevent import GeventSubscriptionServer
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from rx import Observable
from flask_graphql import GraphQLView
from src import db, PostObject, UserObject, CreatePost


basedir = os.path.abspath(os.path.dirname(__file__))
# app initialization
app = Flask(__name__)
app.debug = True
sockets = Sockets(app)


# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# init db
db.init_app(app)


# Combine schemas
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()

# example subscription class


class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


class Subscription(graphene.ObjectType):

    count_seconds = graphene.Int(up_to=graphene.Int())

    random_int = graphene.Field(RandomType)

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

# subscription setup
subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'


# Routes

@app.route('/')
def index():
    return '<p> Hello World</p>'


@sockets.route('/subscriptions')
def echo_socket(ws):
    subscription_server.handle(ws)
    return []


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,  # for having the GraphiQL interface,
        allow_subscriptions=True
    )
)


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
