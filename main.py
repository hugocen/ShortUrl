from flask import Flask, request, jsonify, redirect, abort
import configparser
from urlShortener import urlShortener
import logging


FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('shorturl')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('shorturl.log')
formatter = logging.Formatter(FORMAT)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

config = configparser.ConfigParser()
config.read("config.ini") 

app = Flask(__name__)
app.debug = True
shortener = urlShortener(config, logger)

@app.route("/shortURL", methods=['POST'])
def shorten_request():
	"""
	Get the shorten request from client.
	"""
	data = request.get_json()
	chk_url_res = shortener.valid_url(data["url"])
	if chk_url_res["State"] != "Success":
		return jsonify(chk_url_res)

	result = shortener.generate_shorturl(data["url"])
	if result["State"] != "Success":
		return jsonify(result), 400
	return jsonify(result), 200

@app.route("/<url_key>")
def redirect_to_url(url_key):
	"""
	Check the url_key is in DB, redirect to original url.
	"""
	url = shortener.get_url(url_key)
	if url is None:
		return jsonify({"State": "Failed", 
						"Info": "url_key: '%s' is not in database" % (url_key)}), 404
	return redirect(url)


@app.route("/")
def page():
	"""
	Guide page
	"""
	return "A short url api service."

if __name__ == '__main__':
	# Test with Flask development server
	app.run(host='localhost', port=8080)	
