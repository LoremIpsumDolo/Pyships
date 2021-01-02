import json
import sqlite3

import requests

from app import handler as h

DB = h.Conf.get_database()
application_id = h.Conf.get_application_id()


def get_latest_version():
	conn = sqlite3.connect(DB)
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
	Version = c.fetchall()
	return Version[0][0]


def get_game_version():
	url = 'https://api.worldofwarships.eu/wows/encyclopedia/info/?fields=game_version&'
	r = requests.get(url + str(application_id))
	reply = json.loads(r.text)
	Version = reply['data']['game_version']

	return Version


def insert_meta(n, t, v):
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	c.execute("""
		INSERT OR IGNORE INTO
			tbl_meta
		VALUES (
			:id,
			:version,
			:nation,
			:count )
			""", {
			'id'     : None,
			'version': v,
			'nation' : n,
			'count'  : t
	})
	conn.commit()


def update_radar():
	f = open("app/radar.txt", "r")
	radar_list = f.read().split(',')

	for id in radar_list:
		conn = sqlite3.connect(DB)
		c = conn.cursor()
		c.execute("""
		UPDATE
			tbl_ships
		SET
			radar = '1'
		WHERE
			ship_id=:id
		""", {
				'id': id
		})
		conn.commit()


def select_radar():
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	c.execute("""
		SELECT
			*
		FROM
			tbl_ships
		WHERE
			radar='1'
		""")

	print(c.fetchall())


def insert_values(Vdata):
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	for value in Vdata:
		c.execute("""
			INSERT OR IGNORE INTO
				tbl_ships
			VALUES (
				:ship_name,
				:ship_id_str,
				:nation,
				:ship_id,
				:tier,
				:type,
				:type_short,
				:radar )
				""", {
				'ship_name'  : value['name'],
				'ship_id_str': value['ship_id_str'],
				'nation'     : value['nation'],
				'ship_id'    : value['ship_id'],
				'tier'       : value['tier'],
				'type'       : value['type'],
				'type_short' : value['type_short'],
				'radar'      : None
		})
		conn.commit()


def get_nations():
	ship_nations = []
	r = requests.get('https://api.worldofwarships.eu/wows/encyclopedia/info/?' +
	                 application_id + '&fields=ship_nations')
	r_response = json.loads(r.text)

	for key in r_response['data']['ship_nations'].keys():
		ship_nations.append(key)

	return ship_nations


def get_ships_per_nation(ShipNations):
	CompleteList = []
	url = 'https://api.worldofwarships.eu/wows/encyclopedia/ships/?'

	for nation in ShipNations:
		r = requests.get(url + application_id + '&nation=' + nation +
		                 '&fields=type%2C+name%2C+ship_id%2C+ship_id_str%2C+tier%2C+nation')
		r_response = json.loads(r.text)

		ShipList = []
		for ship_id in r_response['data']:

			if r_response['data'][ship_id]['name'].startswith('['):
				r_response['data'][ship_id]['name'] = str(
						r_response['data'][ship_id]['name'])[1:-1]

			if r_response['data'][ship_id]['type'] == 'Cruiser':
				r_response['data'][ship_id]['type_short'] = 'cc'

			if r_response['data'][ship_id]['type'] == 'Destroyer':
				r_response['data'][ship_id]['type_short'] = 'dd'

			if r_response['data'][ship_id]['type'] == 'AirCarrier':
				r_response['data'][ship_id]['type_short'] = 'cv'

			if r_response['data'][ship_id]['type'] == 'Battleship':
				r_response['data'][ship_id]['type_short'] = 'bb'

			ShipList.append(r_response['data'][ship_id])

		NList = [{
				'nation': nation,
				'total' : r_response['meta']['total'],
				'ships' : ShipList
		}]

		CompleteList.append(NList)

	return CompleteList


def update_ship_db():
	ShipNations = get_nations()
	CompleteList = get_ships_per_nation(ShipNations)
	GameVersion = get_game_version()

	print('Updating to Version :', GameVersion)

	try:
		for nation in CompleteList:

			for ship in nation:
				Vdata = ship['ships']
				insert_values(Vdata)

			n = nation[0]['nation']
			t = nation[0]['total']
			v = GameVersion

			insert_meta(n, t, v)

			print('updated:', nation[0]['nation'], nation[0]['total'])

		return True

	except:

		return False
