import logging

from src.session.session_type import SessionType

logger = logging.getLogger("session_resolver")


def resolve_sessions(self, info):
	query = SessionType.get_query(info)
	session_count = query.count()
	all_sessions = query.all()
	logger.debug("returning %s sessions...", session_count)
	return all_sessions
