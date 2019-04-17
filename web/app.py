#!/usr/bin/env python3

from flask import Flask, render_template, g, jsonify
from jinja2 import Template
from flask import redirect, url_for
import sqlalchemy
import pymysql
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__, static_url_path="/static/", template_folder="templates")
app.config.from_object("config")

def connect_db():
    return create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(app.config["USER"], app.config["PASSWORD"],
                                                                 app.config["DBURL"], app.config["PORT"],
                                                                 app.config["DB"]))

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = connect_db()
    return db


@app.route("/")
def root():
    templ = "tindex.html"
    title = "Dublin Bike Map"
    return render_template(templ,  title=title, KEY_ID=app.config["KEY_ID"], GMAPS_KEY=app.config["GMAPS_KEY"])


@app.route("/station/<int:station_id>")
# in URL bar enter 'station/<number>
def station(station_id):
    engine = get_db()
    li = []
    rows = engine.execute("""SELECT * FROM availability1 WHERE 
                                last_update = (SELECT MAX(last_update)
                                    FROM availability1 
                                        WHERE stationNUM = {})""".format(station_id))
    for row in rows:
        li.append(dict(row))
    engine.dispose()
    return jsonify(lateststationdata=li)



# Inexplicably doesn't work
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, "_database", None)
#     if db is not None:
#         db.close()

@app.route("/stations")
def get_stations():
    engine = get_db()
    li = []
    rows = engine.execute("SELECT * FROM stations1")
    for row in rows:
        li.append(dict(row))
    engine.dispose()
    return jsonify(available=li)


@app.route("/bikestands")
def get_bikestands():
    engine = get_db()
    li = []
    rows = engine.execute("SELECT name, bike_stands FROM stations1")
    for row in rows:
        li.append(dict(row))
    engine.dispose()
    return jsonify(available=li)

# Retrieve by station ID (number)
@app.route("/sot/<int:station_id>")
def get_station_occupancy_timeline(station_id):
    engine = get_db()
    df = pd.read_sql_query("select * from availability1 where stationNUM = {}".format(station_id), engine)
    # params={"num": station_id})
    df['last_update_date'] = pd.to_datetime(df["last_update"], unit='ms', origin="unix")
    df.set_index('last_update_date', inplace=True)
    sample = '1D'
    occupancy = df["available_bike_stands"].resample(sample).mean()
    availability = df['available_bikes'].resample(sample).mean()
    engine.dispose()
    return jsonify(occupancy=occupancy.to_json(), availability=availability.to_json())


# Retrieve by station name
@app.route("/sot/<string:station_name>")
def get_station_occupancy_timeline_byName(station_id):
    engine = get_db()
    df = pd.read_sql_query("select * from availability1 where stationNUM = {}".format(station_id), engine)
    # params={"num": station_id})
    df['last_update_date'] = pd.to_datetime(df["last_update"], unit='ms', origin="unix")
    df.set_index('last_update_date', inplace=True)
    sample = '1D'
    occupancy = df["available_bike_stands"].resample(sample).mean()
    availability = df['available_bikes'].resample(sample).mean()
    engine.dispose()
    return jsonify(occupancy=occupancy.to_json(), availability=availability.to_json())


if __name__ == "__main__":
    app.run(debug=True)
