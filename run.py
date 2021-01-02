import logging
import webbrowser

from app import app

# logging.basicConfig(filename='debug.log', level=logging.INFO,
#                     format='%(levelname)s:%(name)s:%(message)s')

if __name__ == '__main__':
	webbrowser.open("http://localhost:8000/")
	app.run(host="localhost", port=8000, debug=False)
