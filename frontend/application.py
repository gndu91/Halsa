from flask import Flask, render_template, request, make_response
from frontend.localization import get_localization_strings
from flask.ext.babel import format_datetime
from datetime import datetime
from flask.ext.babel import gettext, ngettext

app = Flask(__name__)
app.config.from_pyfile('frontend.cfg')

from flask import g, request
from flask_babel import Babel

babel = Babel(app)


@babel.localeselector
def get_locale():
	# if a user is logged in, use the locale from the user settings
	user = getattr(g, 'user', None)
	if user is not None:
		return user.locale
	# otherwise try to guess the language from the user accept
	# header the browser transmits.  We support de/fr/en in this
	# example.  The best match wins.
	return request.accept_languages.best_match(['de', 'fr', 'en'])


@babel.timezoneselector
def get_timezone():
	user = getattr(g, 'user', None)
	if user is not None:
		return user.timezone


@app.route('/translator')
def translator():
	return '<br>'.join((
		gettext(u'A simple string'),
		gettext(u'Value: %(value)s', value=42),
		ngettext(u'%(num)s Apple', u'%(num)s Apples', 59)
	))


@app.route('/current-date')
def current_date():
	return '<br>'.join((
		format_datetime(datetime.now()),
		format_datetime(datetime.now(), 'full'),
		format_datetime(datetime.now(), 'short')
	))


@app.route('/getcookie')
def getcookie():
	name = request.cookies.get('userID')
	return '<h1>welcome ' + name + '</h1>'


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
	resp = make_response(render_template('readcookie.html'))
	if request.method == 'POST':
		user = request.form['nm']
		resp.set_cookie('userID', user)

	return resp


@app.route('/')
def index():
	return render_template(
		"index.html",
		username="Username",
		logged_in=False,
		**get_localization_strings()
	)


@app.route('/profile')
def profile():
	return render_template(
		"index.html",
		username="Username",
		logged_in=False,
		**get_localization_strings()
	)


@app.route('/login.html')
@app.route('/login')
def login():
	return render_template(
		"login.html",
		**get_localization_strings()
	)


@app.route('/simulation.html')
@app.route('/simulation')
def simulation():
	return render_template(
		"simulation.html",
		**get_localization_strings()
	)


@app.route('/link')
def mylink():
	return repr(request.accept_languages)


if __name__ == "__main__":
	app.debug = True
	app.run(port=5000, debug=True)
