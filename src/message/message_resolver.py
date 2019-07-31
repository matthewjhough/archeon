import logging

from src.message.message_model import MessageModel

logger = logging.getLogger("message_resolver")


def resolve_messages(self, info, user_id):
	# TODO: CHECK USER_ID + SESSION_ID TO RETURN MESSAGES IN SESSION
	logger.debug("fetching messages for user_id: %s", user_id)
	message_query = MessageModel.query.filter_by(user_id=user_id)
	message_count = message_query.count()
	all_messages = message_query.all()
	logger.debug("returning %s messages...", message_count)
	return all_messages
