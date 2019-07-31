import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.session.session_model import SessionModel

logger = logging.getLogger("gql_types")
relay = graphene.relay


class SessionType(SQLAlchemyObjectType):
	class Meta:
		model = SessionModel
		interfaces = (relay.Node,)
