import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.message.message_model import MessageModel

relay = graphene.relay


class MessageType(SQLAlchemyObjectType):
	class Meta:
		model = MessageModel
		interfaces = (relay.Node,)
