"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

from tracemalloc import start

import flask
from flask import request, Flask, jsonify, render_template, request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    km = request.args.get("km", type=float)
    brevet = request.args.get("brevet_dist_km", type=float)
    begin_date = request.args.get("begin_date", "")
    begin_time = request.args.get("begin_time", "")
    offset = request.args.get("utc_offset", "+00:00")

    if km is None or brevet is None:
        return "Enter valid distances", 400

    start = arrow.get(f"{begin_date}T{begin_time}{offset}").isoformat()

    opening = acp_times.open_time(km, brevet, start)
    closing = acp_times.close_time(km, brevet, start)
    result = {
        "open": opening,
        "close": closing,
    }

    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
