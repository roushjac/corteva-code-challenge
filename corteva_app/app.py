from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from corteva_app.database.mgmt import db_session, conn_string

# create Flask's SQLAlchemy extension object
db = SQLAlchemy()

# initialize the main Flask object with the special dunder variable __name__
# we will use this to define API routes and set app configs
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn_string

# initialize the app with the extension
db.init_app(app)

# this should close open database connections when requests complete or the app shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# allow user to specify station id and date
@app.route("/api/weather", methods=["GET"])
def get_weather():
    args = request.args
    station_id: str = args.get("station_id", type=str)
    date: str = args.get("date", type=str)

    if None not in (station_id, date):
        # both paremeters are specified
        pass
    elif station_id:
        pass
    elif date:
        pass
    else:
        # return empty result if nothing is specified - too much data to return everything
        result = {}

    return result

# allow user to specify year
@app.route("/api/yield", methods=["GET"])
def get_yield():
    args = request.args
    year: int = args.get("year", type=int)
    
    if year:
        pass
    else:
        # return everything from the table
        result = {}

    return result

# allow user to specify station id and year
@app.route("api/weather/stats", methods=["GET"])
def get_weather_stats():
    args = request.args
    station_id: str = args.get("station_id", type=str)
    year: int = args.get("year", type=int)
    
    if None not in (station_id, year):
        pass
    elif station_id:
        pass
    elif year:
        pass
    else:
        # return everything from the table
        result = {}

    return result