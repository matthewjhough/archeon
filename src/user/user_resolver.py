import logging

from src.user.user_model import UserModel

logger = logging.getLogger("user_resolver")


def resolve_user(self, info, user_id):
	logger.info("getting user, with id %s", user_id)
	user = UserModel.query.filter(UserModel.uuid == user_id).first()
	logger.info("returning user: %s", user)
	return user
