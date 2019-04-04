from flask import Flask, current_app,request,render_template,url_for,jsonify,g
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
# import sys
# print(sys.modules)
# import sqlalchemy
# [name for name in sys.modules if 'sqlalchemy' in name]


app = Flask(__name__,
            static_url_path="/static",  
            static_folder="static",  
            template_folder="templates",  
            )

class Config(object):
    DEBUG = True


app.config.from_object(Config)


@app.route("/index", methods=["GET","POST"])
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
    rows = engine.execute("SELECT * from stations1;")
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





if __name__ == '__main__':
    # app.run()
    app.run(host="127.0.0.1", port=5000, debug=True)