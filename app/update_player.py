import json

import requests

from app import handler as h, sql_player

application_id = h.Conf.get_application_id()


def get_account_id(player_name):
	URL_a = 'https://api.worldofwarships.eu/wows/account/list/?'
	r = requests.get(URL_a + application_id + '&type=exact&search=' +
	                 player_name + '&fields=account_id%2C+nickname')
	account_id = json.loads(r.text)
	for data in account_id['data']:
		return data['account_id']


def parse_logfile(battle_timestamp, replayFile):
	ParsedLogData = []
	for player in replayFile['vehicles']:

		if player['name'].startswith(':'):
			account_id = None
			Bot = 'True'
		else:
			account_id = get_account_id(player['name'])
			Bot = 'False'

		if player['relation'] == 2:
			relation = 'B'
		elif player['relation'] == 1:
			relation = 'A'
		elif player['relation'] == 0:
			relation = 'A'
		# else:
		# 	pass

		ship_id = player['shipId']
		shipdata = sql_player.get_ship_data(ship_id)

		if account_id is None:
			account_id = 'null'

		print(ship_id, account_id)

		values = {
				'battle_timestamp': battle_timestamp,
				'player_id'       : player['id'],
				'account_id'      : account_id,
				'player_name'     : player['name'],
				'Bot'             : Bot,
				'relation'        : relation,
				'ship_name'       : shipdata['ship_name'],
				'ship_id'         : ship_id,
				'ship_type_short' : shipdata['ship_type_short'],
				'ship_type_long'  : shipdata['ship_type']
		}
		ParsedLogData.append(values)

	return ParsedLogData


def request_all_playerstats(account_id_list):
	URL_es = 'https://api.worldofwarships.eu/wows/account/info/?'
	joined_string = '%2C+'.join(account_id_list)
	r = requests.get(URL_es + application_id + '&account_id=' + joined_string +
	                 '&fields=nickname%2C+statistics.pvp.battles%2C+statistics.pvp.wins')
	pvp_stats = json.loads(r.text)
	return pvp_stats


def request_shipstats(stat, nickname, ParsedLogfile):
	URL_PS = 'https://api.worldofwarships.eu/wows/ships/stats/?'

	for field in ParsedLogfile:
		if field['player_name'] == nickname:
			ship_id = str(field['ship_id'])
			ShipURL = (URL_PS + application_id + '&account_id=' + stat +
			           '&fields=pvp.battles%2C+pvp.wins&ship_id=' + ship_id)

	r = requests.get(ShipURL)
	PlayerShipStats = json.loads(r.text)
	return PlayerShipStats


def get_player_stats(ParsedLogfile):
	account_id_list = []
	parsed_player_stats = []

	for field in ParsedLogfile:

		if field['account_id'] == 'null' or field['Bot'] == 'True':
			pass
		else:
			account_id = str(field['account_id'])
			account_id_list.append(account_id)

	pvp_stats = request_all_playerstats(account_id_list)

	for stat in pvp_stats['data']:
		stat = str(stat)
		nickname = pvp_stats['data'][stat]['nickname']

		PlayerShipStats = request_shipstats(stat, nickname, ParsedLogfile)
		statistics = pvp_stats['data'][stat]['statistics']

		if statistics is not None:
			status = 'public'
			pvp = statistics['pvp']
			TotalBattles = pvp['battles']
			TotalWins = pvp['wins']
			TotalAvg = TotalWins / TotalBattles * 100
			TotalAvg_f = ("{:.2f}".format(TotalAvg) + '%')

			winrate_ship = PlayerShipStats['data'][stat][0]['pvp']['wins']
			battles_ship = PlayerShipStats['data'][stat][0]['pvp']['battles']
			avg_ship_t = winrate_ship / battles_ship * 100
			avg_ship = ("{:.2f}".format(avg_ship_t) + '%')

		elif statistics is None or statistics == 'null':
			status = 'private'
			TotalBattles = '0'
			TotalWins = '0'
			TotalAvg_f = '0'
			winrate_ship = '0'
			battles_ship = '0'
			avg_ship = '0'

		PlayerList = {
				'status'    : status,
				'account_id': stat,
				'nickname'  : nickname,
				'total'     : {
						'TotalBattles': TotalBattles,
						'TotalWins'   : TotalWins,
						'TotalAvg_f'  : TotalAvg_f,
						'winrate_ship': winrate_ship,
						'battles_ship': battles_ship,
						'avg_ship'    : avg_ship}
		}
		parsed_player_stats.append(PlayerList)

	return parsed_player_stats


def merge(ParsedLogfile, parsed_player_stats):
	ParsedLogfile = ParsedLogfile

	defaultDict = {
			'TotalBattles': '0',
			'TotalWins'   : '0',
			'TotalAvg_f'  : '0',
			'winrate_ship': '0',
			'battles_ship': '0',
			'avg_ship'    : '0'
	}

	for _ParsedLogfile in ParsedLogfile:
		_account_id = str(_ParsedLogfile['account_id'])
		_player_name = _ParsedLogfile['player_name']

		if _ParsedLogfile['account_id'] == 'null' or _ParsedLogfile['account_id'] is None:
			_ParsedLogfile.update(defaultDict)

		else:
			for _parsed_player_stats in parsed_player_stats:
				_List_account_id = str(_parsed_player_stats['account_id'])

				if _List_account_id == _account_id:
					_ParsedLogfile.update(_parsed_player_stats['total'])

	h.save_as_json("app/final_list.json", ParsedLogfile)
	return ParsedLogfile


def update_player():
	replayFile = h.open_json(h.Conf.get_replay_file())
	battle_timestamp = replayFile['dateTime']

	if not sql_player.check_date(battle_timestamp):

		print('________________________')
		print('TimeStamp: New TimeStamp')
		print('________________________')

		try:
			print('starting: parse_logfile')
			ParsedLogfile = parse_logfile(battle_timestamp, replayFile)
			print('finished: parse_logfile')
			print('________________________')
			# print(json.dumps(ParsedLogfile, indent=4))

			try:
				print('starting: get_player_stats')
				parsed_player_stats = get_player_stats(ParsedLogfile)
				print('finished: get_player_stats')
				print('________________________')
				# print(json.dumps(parsed_player_stats, indent=4))

				try:
					print('starting: merge')
					parsed_result = merge(ParsedLogfile, parsed_player_stats)
					print('finished: merge')
					print('________________________')
					# print(json.dumps(parsed_result, indent=4))

					try:
						print('starting: update_tbl_player')
						sql_player.update_tbl_player(parsed_result)
						print('finished: update_tbl_player')
						print('________________________')
						return True

					except:
						print('error: sql_player.update_tbl_player')
						print('________________________')
						return False

				except:
					print('error: merge')
					print('________________________')
					return False

			except:
				print('error: parsed_player_stats')
				print('________________________')
				return False

		except:
			print('error: ParsedLogfile')
			print('________________________')
			return False

	return True
