import json

import requests

from app import handler as h, sql_player as sql


def check_app_id(application_id):
	url = 'https://api.worldofwarships.eu/wows/encyclopedia/info/?fields=game_version&application_id='
	r = requests.get(url + str(application_id))
	reply = json.loads(r.text)

	default = {'token_status': 'unknown',
	           'game_version': 'unknown'}

	if reply['status'] == 'ok':
		default['token_status'] = 'valid'
		default['game_version'] = reply['data']['game_version']

	elif reply['status'] == 'error':
		if reply['error']['message'] == 'INVALID_APPLICATION_ID':
			default['token_status'] = 'INVALID_APPLICATION_ID'
			default['game_version'] = 'unknown error'
	else:
		default['token_status'] = 'unknown error'
		default['game_version'] = 'unknown error'

	return default


def check_game_root(game_root):
	game_file = str(game_root + '\\WorldOfWarships.exe')
	if h.check_if_file_exist(game_file):
		print('game path: valid')

		replay_dir = str(game_root + '\\replays')
		if h.check_if_file_exist(replay_dir):
			print('replay path: valid')

			app_id_status = check_app_id(h.Conf.get_application_id())
			version = app_id_status['game_version']
			replay_dir_version = str(replay_dir + '\\' + version)

			if h.check_if_file_exist(replay_dir_version):
				print('version folder found')
				replay_file = str(replay_dir_version + '\\tempArenaInfo.json')
			else:
				replay_file = str(replay_dir + '\\tempArenaInfo.json')

			print('replay file:', replay_file)

			db_version = sql.get_db_version()
			config = {
					'game_root'   : game_root,
					'replay_dir'  : replay_dir,
					'replay_file' : replay_file,
					'game_version': version,
					'db_version'  : db_version,
					'database'    : 'app/WoWs.db'
			}

			return config

		else:
			print('replay path: invalid')
			return False

	else:
		print('game path: invalid')
		return False


def check_config():
	application_id = h.Conf.get_application_id()
	replay_file = h.Conf.get_replay_dir()
	config = h.ConfigFile

	default = {
			'stat_config_file': 'invalid',
			'ReplayDir'       : 'invalid',
			'AppId'           : 'invalid',
			'DB_Version'      : 'invalid'
	}

	if h.check_if_file_exist(config):
		default['stat_config_file'] = 'valid'
		print('config OK')
	else:
		print('no config found')

	id_stat = check_app_id(application_id)
	if id_stat['token_status'] == 'valid':
		print('AppId: OK')
		default['AppId'] = 'valid'

		print(sql.get_db_version())
		print(id_stat['game_version'])

		if str(id_stat['game_version']) == str(sql.get_db_version()):
			default['DB_Version'] = 'valid'
			print('DB_Version invalid')

	else:
		default['AppID_status'] = id_stat['token_status']
		print(id_stat['token_status'])

	if replay_file is not None:
		if h.check_if_file_exist(replay_file):
			default['ReplayDir'] = 'valid'
			print('replay OK')
	else:
		print('no valid replay found')

	print(json.dumps(default, indent=4))
	return default
