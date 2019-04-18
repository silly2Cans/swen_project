from flask import Flask, current_app,request,render_template,url_for,jsonify,g
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import InfoWindow
import currentweather
import json
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

import numbers
# import sys
# print(sys.modules)
# import sqlalchemy
# [name for name in sys.modules if 'sqlalchemy' in name]
# import models

app = Flask(__name__,
            static_url_path="/static",  
            static_folder="static",  
            template_folder="templates",  
            )

class Config(object):
    DEBUG = True


app.config.from_object(Config)


@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")


@app.route("/bikeinfo", methods=["GET","POST"])
def bike():
    return render_template("bikeinfo.html")


@app.route("/googlemaps", methods=["GET","POST"])
def maps():
    return render_template("googlemaps.html")



def connect_to_database():
    engine = create_engine("mysql+mysqldb://swen_main_:mixednuts@swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com:3306/dublin_bikes", echo=True)
    return engine
    # //engine ="mysql://swen_main_:mixednuts@swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com:3306/dublin_bikes"
    # //return engine

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.dispose()

@app.route("/stations", methods=["GET","POST"])
def get_stations():
    engine = get_db()
    stations = []
    InfoWindow.avail_to_db()
    rows = engine.execute("SELECT position_lat,position_lon,STATUS, available_bikes , available_bike_stands, stations1.stationNUM,bike_stands,last_update,stations1.name FROM InfoWindow,stations1 WHERE InfoWindow.stationNUM=stations1.stationNUM;")
    for row in rows:
        stations.append(dict(row))
    return jsonify(stations)
    # print(len(stations))
    # return stations
    # for station in stations:
    #     print(station)
    # rows = engine.execute("SELECT * from stations1;")
    # print('#found {} stations', len(rows))
    # return jsonify(stations=[dict(row.items()) for row in rows])


# @app.route("/stations", methods=["GET","POST"])
# def get_stations():
#     conn = pymysql.connect(host='swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com', port=3306, user='swen_main_', password='mixednuts', database='dublin_bikes')
#     cur = conn.cursor()
#     stations = []
#     rows = cur.execute("SELECT * from stations1;")
#     stations=cur.fetchall()[1]
#     # print(len(rows))
#     # sql = "select * from station;"
#     # rows = engine.execute(sql).fetchall()
#     # print('#found {} stations', len(rows))
#     # return jsonify(stations=[dict(row.items()) for row in rows])
#     cur.close()
#     conn.close()
#     # //return jsonify(stations=stations)
#     return jsonify(stations=[stations])
#
@app.route("/currentWeather", methods=["GET","POST"])
def currentWeather():
    weather = currentweather.get_weather()
    dd=weather['weather']
    dd.append(weather['main'])
    dd1=dd[0]
    dd2=dd[1]
    dd1.update(dd2)
    dd1['icon']=dd1['icon']+".png"
    dd1[ 'visibility']=weather['visibility']
    dd1['windspeed']=weather['wind']['speed']
    del dd1['main']
    dd1=json.dumps(dd1)
    # print(dd1)
    # print(type(dd1))
    return dd1



@app.route("/occupancy/<int:station_id>",methods=["GET","POST"])
def get_occupancy(station_id):
    engine = get_db()
    df = pd.read_sql_query("select * from availability2 where stationNUM = %(number)s",
    engine, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    df['available_bike_stands'] = df['available_bike_stands'].astype(int)
    res = df['available_bike_stands'].resample('1d').mean().dropna(how="any")
#res['dt'] = df.index
    # print(res)
    return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index),
res.values))))





@app.route("/station_occupancy_weekly/<int:station_id>",methods=["GET","POST"])
def get_station_occupancy_weekly(station_id):
    conn = get_db()
    days = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    df = pd.read_sql_query("select * from availability2 where stationNUM = "+str(station_id),conn,
    )
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
    df.set_index('last_update_date', inplace=True)
    df['weekday'] = df.index.weekday

    df['available_bike_stands'] = df['available_bike_stands'].astype(int)
    df['available_bikes'] = df['available_bikes'].astype(int)
    mean_available_stands = df[['available_bike_stands',
    'weekday']].groupby('weekday').mean()
    mean_available_bikes = df[['available_bikes', 'weekday']].groupby('weekday').mean()
    mean_available_stands.index = [days[i] for i in df['weekday'].unique()]
    mean_available_bikes.index = [days[i] for i in df['weekday'].unique()]
    print(mean_available_bikes)
    return jsonify(mean_available_stands=mean_available_stands.to_json(),
    mean_available_bikes=mean_available_bikes.to_json())





















@app.route("/predict",methods=["GET","POST"])
def predict():
# now we can call various methods over model as as:
# Let X_test be the feature for which we want to predict the output
#     df = pd.read_csv('C:\stations.csv')
#     cont_features = ['banking', 'bike_stands','bonus', 'last_update']

    if request.method == 'POST':
        Hour = request.form['hour']
        if (int(Hour)<24)&(int(Hour)>=0):
            Hour = Hour
        else :
            return render_template('index.html', myresult="The hour you entered is invalid")
        Day = request.form['dayofweek']
        if (int(Day)<7)&(int(Day)>=0):
            Day = Day
        else :
            return render_template('index.html', myresult="The Day of Week you entered is invalid")
        Station_ID = request.form['Station_ID']
        if (int(Station_ID)<115)&(int(Station_ID)>=2)&(int(Station_ID)!=20):
            Station_ID = Station_ID
        else :
            return render_template('index.html', myresult="The Station_ID you entered is invalid")

        nx = {'hour_1': 0, 'hour_2': 0, 'hour_3': 0, 'hour_4': 0, 'hour_5': 0, 'hour_6': 0, 'hour_7': 0, 'hour_8': 0,
              'hour_9': 0, 'hour_10': 0, 'hour_11': 0, 'hour_12': 0, 'hour_13': 0, 'hour_14': 0, 'hour_15': 0,
              'hour_16': 0, 'hour_17': 0, 'hour_18': 0, 'hour_19': 0, 'hour_20': 0, 'hour_21': 0, 'hour_22': 0,
              'hour_23': 0, 'dayofweek_1': 0, 'dayofweek_2': 0, 'dayofweek_3': 0, 'dayofweek_4': 0, 'dayofweek_5': 0,
              'dayofweek_6': 0}
        num = str(Hour)
        hou = "hour_"
        hou = hou + num
        nx[hou]=1
        Day = str(Day)
        dayw = "dayofweek_"
        dayw= dayw + Day
        nx[dayw]=1
        newx = pd.DataFrame(nx, index=[0])
        num = str(Station_ID)
        sta = "station"
        piclName = sta + num + ".pickle"
        with open('static/models/' + piclName, 'rb') as f:
            lrg2 = pickle.load(f)
            resut=lrg2.predict(newx)[0]
            available_bikes=int(resut)
    return render_template('index.html', myresult =available_bikes,Station_ID=Station_ID)

        # return render_template('index.html', Date=Date,Month=Month,Year=Year,Station=Station,Station_ID=Station_ID)

# return jsonify(result)






if __name__ == '__main__':
    # app.run()
    app.run(host="127.0.0.1", port=5000, debug=True)