import sqlite3

from app import handler as h

database = h.Conf.get_database()
replayFile = h.Conf.get_replay_file()


## META ##

def sql_select_everything(table):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	query = str("SELECT * FROM " + table)
	c.execute(query)
	return c.fetchall()


def get_db_version():
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""
		SELECT DISTINCT
			version
		FROM
			tbl_meta
		ORDER BY
			id
		DESC LIMIT 1
		""")
	Date = c.fetchall()
	return Date[0][0]


def get_last_date():
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""
		SELECT DISTINCT
			battle_timestamp
		FROM
			tbl_player
		ORDER BY
			id
		DESC LIMIT 1
		""")
	Date = c.fetchall()
	return Date[0][0]


def check_date(battle_timestamp):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""
		SELECT DISTINCT
			battle_timestamp
		FROM
			tbl_player
		WHERE
			battle_timestamp=?
		""", (battle_timestamp,)
	          )

	for i in c.fetchall():
		return i


## META END ##


def make_tbl_player():
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""
	CREATE TABLE IF NOT EXISTS
		tbl_player (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			battle_timestamp VARCHAR DEFAULT 0,
			player_id TEXT DEFAULT 0,
			player_name VARCHAR DEFAULT 0,
			Bot VARCHAR DEFAULT 1,
			relation VARCHAR DEFAULT 0,
			ship_name TEXT DEFAULT 0,
			ship_id VARCHAR DEFAULT 0,
			ship_type_short VARCHAR DEFAULT 0,
			ship_type_long VARCHAR DEFAULT 0,
			TotalBattles VARCHAR DEFAULT 0,
			TotalWins VARCHAR DEFAULT 0,
			TotalAvg_f VARCHAR DEFAULT 0,
			winrate_ship VARCHAR DEFAULT 0,
			battles_ship VARCHAR DEFAULT 0,
			avg_ship VARCHAR DEFAULT 0,
			UNIQUE (
				battle_timestamp,
				player_id )
			);""")
	conn.commit()


def get_ship_data(ship_id):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("""
		SELECT
			ship_name,
			type,
			type_short
		FROM
			tbl_ships
		WHERE
			ship_id=?
		""", (ship_id,)
	          )
	rows = c.fetchall()
	data = {
			'ship_name'      : rows[0][0],
			'ship_type'      : rows[0][1],
			'ship_type_short': str(rows[0][2] + '.png')
	}
	return data


def update_tbl_player(parsed_result):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	for value in parsed_result:
		c.execute("""
		INSERT OR IGNORE INTO
			tbl_player
		VALUES (
			:id,
			:battle_timestamp,
			:player_id,
			:player_name,
			:Bot,
			:relation ,
			:ship_name,
			:ship_id,
			:ship_type_short,
			:ship_type_long,
			:TotalBattles,
			:TotalWins,
			:TotalAvg_f,
			:winrate_ship,
			:battles_ship,
			:avg_ship )
				""", {
				'id'              : None,
				'battle_timestamp': value['battle_timestamp'],
				'player_id'       : value['player_id'],
				'player_name'     : value['player_name'],
				'Bot'             : value['Bot'],
				'relation'        : value['relation'],
				'ship_name'       : value['ship_name'],
				'ship_id'         : value['ship_id'],
				'ship_type_short' : value['ship_type_short'],
				'ship_type_long'  : value['ship_type_long'],
				'TotalBattles'    : value['TotalBattles'],
				'TotalWins'       : value['TotalWins'],
				'TotalAvg_f'      : value['TotalAvg_f'],
				'winrate_ship'    : value['winrate_ship'],
				'battles_ship'    : value['battles_ship'],
				'avg_ship'        : value['avg_ship']})
		conn.commit()


def get_final_results(battle_timestamp, relation):
	conn = sqlite3.connect(database)
	c = conn.cursor()

	def radar_check(ship_name):
		c.execute("""
			SELECT DISTINCT
				radar
			FROM
				tbl_ships
			WHERE
				ship_name=:ship_name
			""", {
				'ship_name': ship_name
		})
		for r in c.fetchall():
			return r[0]

	Type = ('AirCarrier', 'Battleship', 'Cruiser', 'Destroyer')
	result = []
	for ship_type_long in Type:
		ship_type_long = ship_type_long

		c.execute("""
			SELECT
				player_name,
				ship_name,
				ship_type_short,
				TotalAvg_f,
				TotalBattles,
				avg_ship,
				battles_ship,
				relation
			FROM
				tbl_player
			WHERE
				battle_timestamp=:battle_timestamp
			AND
				relation=:relation
			AND
				ship_type_long=:ship_type_long
			""", {
				'battle_timestamp': battle_timestamp,
				'relation'        : relation,
				'ship_type_long'  : ship_type_long
		})

		for i in c.fetchall():
			_res = i

			if radar_check(_res[1]) is None:
				radar = 'noradar'
			else:
				radar = 'radar'

			res = {
					'player_name'    : _res[0],
					'ship_name'      : _res[1],
					'ship_type_short': _res[2],
					'TotalAvg_f'     : _res[3],
					'TotalBattles'   : _res[4],
					'avg_ship'       : _res[5],
					'battles_ship'   : _res[6],
					'relation'       : _res[7],
					'radar'          : radar
			}
			result.append(res)
	return result


def get_avg_team_score(values):
	sum_num = 0
	for i in values:
		j = i['TotalAvg_f'].strip('%')
		sum_num = sum_num + float(j)

	avg = sum_num / len(values)
	return round(avg, 2)


def get_mvp(values):
	mvp_score = float(0)
	mvp = ""
	for i in values:
		score = float(i['TotalAvg_f'].strip('%'))
		# player = i['player_name']
		if score >= mvp_score:
			mvp_score = score
			mvp = i['player_name']
		else:
			pass

	return mvp


def build_table(LocalDate):
	resultA = get_final_results(LocalDate, 'A')
	resultA_avg = get_avg_team_score(resultA)
	team_A_mvp = get_mvp(resultA)
	print('team_A_mvp:', team_A_mvp)
	print('Team A avg :', resultA_avg)

	resultB = get_final_results(LocalDate, 'B')
	resultB_avg = get_avg_team_score(resultB)
	team_B_mvp = get_mvp(resultB)
	print('team_B_mvp:', team_B_mvp)
	print('Team B avg :', resultB_avg)

	Rows = []

	for x in range(len(resultA)):

		if resultA[x]['TotalAvg_f'] <= resultB[x]['TotalAvg_f']:
			resultA[x]["playerA_avgClass"] = 'red wr'
			resultB[x]["playerA_avgClass"] = 'green wr'
		else:
			resultA[x]["playerA_avgClass"] = 'green wr'
			resultB[x]["playerA_avgClass"] = 'red wr'

		row = {
				'playerA_name'        : resultA[x]['player_name'],
				'playerB_name'        : resultB[x]['player_name'],
				'playerA_ship_name'   : resultA[x]['ship_name'],
				'playerB_ship_name'   : resultB[x]['ship_name'],

				'playerA_type'        : resultA[x]['ship_type_short'],
				'playerB_type'        : resultB[x]['ship_type_short'],
				'radarA'              : resultA[x]['radar'],
				'radarB'              : resultB[x]['radar'],

				'playerA_avg'         : resultA[x]['TotalAvg_f'],
				'playerB_avg'         : resultB[x]['TotalAvg_f'],
				'playerA_TotalBattles': resultA[x]['TotalBattles'],
				'playerB_TotalBattles': resultB[x]['TotalBattles'],
				'playerA_ShipAvg'     : resultA[x]['avg_ship'],
				'playerB_ShipAvg'     : resultB[x]['avg_ship'],
				'playerA_ShipBattles' : resultA[x]['battles_ship'],
				'playerB_ShipBattles' : resultB[x]['battles_ship'],
				'playerA_avgClass'    : resultA[x]['playerA_avgClass'],
				'playerB_avgClass'    : resultB[x]['playerA_avgClass'],
		}
		Rows.append(row)
	Export = [
			{
					'date'      : LocalDate,
					'team_A_avg': resultA_avg,
					'team_A_mvp': str(team_A_mvp),
					'team_B_avg': resultB_avg,
					'team_B_mvp': str(team_B_mvp)
			},
			{
					'data': Rows
			}]
	return Export
