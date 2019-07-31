import logging

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from src.user.user_model import UserModel

logger = logging.getLogger("gql_types")
relay = graphene.relay


# Types


class UserType(SQLAlchemyObjectType):
	class Meta:
		model = UserModel
		interfaces = (relay.Node,)
