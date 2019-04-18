#! usr/bin/env python3
import requests
import json
from pprint import pprint
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
import simplejson as simjson
import time
import datetime
# from IPython.display import display
import pymysql

CONTRACT = 'Dublin'
APIKEY = '7b9a350297fefef5f4147e65b6bc3114aacde014'
STATIONS = 'https://api.jcdecaux.com/vls/v1/stations'
DBURL = 'swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com'
PORT = '3306'
DB = 'dublin_bikes'
USER = 'swen_main_'
PASSWORD = 'mixednuts'

def avail_to_db():
    tm = time.time_ns()
    # print(tm)
    f="%Y-%m-%d %H:%M:%S"
    request = requests.get(STATIONS, params={'contract':CONTRACT,'apiKey':APIKEY})
    availability = json.loads(request.text)
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, DBURL, PORT, DB))
    engine.execute("DELETE FROM InfoWindow;")
    for data in availability:
        ts=str(data.get('last_update'))
        ts=float(ts[:10]+"."+ts[10:])
        data_points = (data.get('number'), data.get('available_bikes'), data.get('available_bike_stands'),
                       datetime.datetime.fromtimestamp(ts), int(data.get('number')*tm), int(tm))
        engine.execute("INSERT INTO InfoWindow values (%s,%s,%s,%s,%s,%s)", data_points)
#         print(data_points)
#         print("%s,%s,%s,%s,%s,%s" % data_points)
        engine.dispose()

# while True:
#     avail_to_db()
#     time.sleep(5*60)
#
avail_to_db()
