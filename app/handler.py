import json
import pathlib

ConfigFile = 'app/config.json'
TokenFile = 'app/token.json'


def check_if_file_exist(file):
	try:
		if pathlib.Path(file).exists():
			return True
		else:
			return False
	except:
		print('error: open file')
		# return False


def save_as_json(file_path, contend):
	try:
		with open(file_path, 'w', encoding="utf-8") as outfile:
			json.dump(contend, outfile, ensure_ascii=False)
		print('success: save_as_json')
		return True
	except:
		print('error: save_as_json')
		return False


def open_json(file_path):
	try:
		file_contend = open(file_path, "r", encoding="utf-8")
		contend_data = json.load(file_contend)
		file_contend.close()
		return contend_data
	except:
		print('error: open_json')
		return False


class Conf:

	@classmethod
	def get_game_root(cls):
		try:
			f = open_json(ConfigFile)
			game_root = f['game_root']
			return game_root
		except:
			return False

	@classmethod
	def get_replay_file(cls):
		try:
			f = open_json(ConfigFile)
			replay_file = f['replay_file']
			return replay_file
		except:
			return False

	@classmethod
	def get_replay_dir(cls):
		try:
			f = open_json(ConfigFile)
			replay_dir = f['replay_dir']
			return replay_dir
		except:
			return False

	@classmethod
	def get_application_id(cls):
		try:
			f = open_json(TokenFile)
			application_id = f['application_id']
			return application_id
		except:
			return False

	@classmethod
	def get_database(cls):
		try:
			f = open_json(ConfigFile)
			database = f['database']
			return database
		except:
			return False

	@classmethod
	def get_game_version(cls):
		try:
			f = open_json(ConfigFile)
			game_version = f['game_version']
			return game_version
		except:
			return False
