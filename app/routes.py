from flask import render_template, redirect, url_for, request, jsonify

from app import app, handler as h, setup_check, sql_player as sql, db_updater, update_player


###################################
#       Render Templates         #
###################################


@app.route('/')
def url_base():
	for v in setup_check.check_config().values():
		if v != 'valid':
			return redirect(url_for('url_settings'))
	else:
		return redirect(url_for('url_home'))


@app.route('/home')
def url_home():
	Versions = setup_check.get_app_versions()
	return render_template('table/table-wrapper.html', app_version=Versions['current'], git_version=Versions['latest'])


@app.route('/chart')
def url_chart():
	Title = 'Chart'
	return render_template('chart/chart.html', Title=Title)


@app.route('/settings', methods=['GET', 'POST'])
def url_settings():
	Title = 'Settings'
	Field = ['ReplayDir', 'AppID']
	Database = 'db_status'
	return render_template('settings/settings.html', Field=Field, Title=Title, Database=Database)


@app.route('/table')
def url_table():
	Title = 'Table'
	Rows = sql.build_table(sql.get_last_date())
	print(Rows[1]['data'])
	return render_template('table/table.html', Title=Title, Rows=Rows[1]['data'], ID=Rows[0]['date'])


#########################################
#           API endpoints               #
#########################################

#########################
#        Status         #
#########################


@app.route('/poll', methods=['GET'])
def url_poll():
	replayFile = h.Conf.get_replay_file()
	if h.check_if_file_exist(replayFile):
		try:
			TimeStamp = h.open_json(replayFile)
			return TimeStamp['dateTime']
		except:
			return 'noFile'
	else:

		return 'noFile'


#########################
#        UPDATE         #
#########################


@app.route('/update', methods=['GET'])
def url_update():
	if update_player.update_player():
		return 'TABLE UPDATED'
	else:
		return 'error'


#########################
#        Settings       #
#########################


@app.route('/status', methods=['GET', 'POST'])
def url_status():
	if request.method == 'POST':
		r = request.form.get('request')

		if r == 'get_status':
			return jsonify(setup_check.check_config())

		elif r == 'get_log':
			return jsonify(h.open_json(h.ConfigFile))
	else:
		pass


#########################
#        ReplayDir      #
#########################


@app.route('/ReplayDir', methods=['GET', 'POST'])
def url_validate_ReplayDir():
	if request.method == 'POST':
		r = request.form.get('request')
		v = request.form.get('value')

		if r == 'validate_ReplayDir' and v is not None:
			if setup_check.check_game_root(v):
				return 'valid'
			else:
				return 'invalid'

		elif r == 'save_ReplayDir' and v is not None:
			config = setup_check.check_game_root(v)
			if setup_check.check_game_root(v):
				h.save_as_json(h.ConfigFile, config)
				return 'valid'
		else:
			return 'invalid'
	else:
		pass


#########################
#        AppID          #
#########################


@app.route('/AppID', methods=['GET', 'POST'])
def url_validate_AppID():
	if request.method == 'POST':
		r = request.form.get('request')
		v = request.form.get('value')

		if r == 'validate_AppID' and v is not None:
			AppID = setup_check.check_app_id(v)['token_status']
			if AppID == 'ok':
				return 'valid'
			else:
				return AppID

		elif r == 'save_AppID' and v is not None:
			AppID = setup_check.check_app_id(v)['token_status']
			if AppID == 'ok':
				NewTokenfile = {"application_id": v}
				h.save_as_json(h.TokenFile, NewTokenfile)
				return 'valid'
			else:
				return AppID
		else:
			return 'invalid'
	else:
		pass


#########################
#        DB UPDATE      #
#########################

@app.route('/update_db', methods=['GET', 'POST'])
def url_update_db():
	try:
		db_updater.update_ship_db()
		return 'updated'
	except:
		return 'error'
