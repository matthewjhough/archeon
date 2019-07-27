import os


def set_logging_path(folder, path):
	if not os.path.exists(folder):
		os.makedirs(folder)

	return path
