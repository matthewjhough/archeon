import logging
import os

from flask import Flask
from flask_graphql import GraphQLView
from flask_sockets import Sockets
from graphql_ws.gevent import GeventSubscriptionServer

from src.common.db import db
from src.schema import schema
from utils.logging import set_logging_path

basedir = os.path.abspath(os.path.dirname(__file__))

# logging setup
logging.basicConfig(
	filename=set_logging_path('logs', 'logs/server.log'),
	level=logging.INFO,
	format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)
logger = logging.getLogger("app")
logger.info("starting server...")

# app initialization
app = Flask(__name__)
app.debug = True
sockets = Sockets(app)

# configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# init db
db.init_app(app)

# subscription setup
subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'


# routes

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
