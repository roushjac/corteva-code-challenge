from typing import List

from flask import Flask, request, jsonify
from corteva_app.database.mgmt import conn_string, db
from corteva_app.database.models import Weather, Yield, WeatherStats

# initialize the main Flask object with the special dunder variable __name__
# we will use this to define API routes and set app configs
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = conn_string

# initialize the app with the extension
db.init_app(app)


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
        # get result as a list even though it's a single result. makes it easier to construct result
        result: List[Yield] = db.session.execute(db.select(Yield).filter_by(year=year)).scalars().fetchall()
    else:
        # return everything from the table
        result: List[Yield] = db.session.execute(db.select(Yield)).scalars().fetchall()

    response = {
        "status": 200,
        "data": [{
            "year": q.year,
            "total_grain_yield": q.total_grain_yield
        } for q in result]
    }

    return jsonify(response)

# allow user to specify station id and year
@app.route("/api/weather/stats", methods=["GET"])
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