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
from IPython.display import display
#import mysql
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
    request = requests.get(STATIONS, params={'contract':CONTRACT,'apiKey':APIKEY})
    availability = json.loads(request.text)
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, DBURL, PORT, DB))
    for data in availability:
        data_points = (data.get('number'), data.get('available_bikes'), data.get('available_bike_stands'), 
                       data.get('last_update'), data.get('number')*data.get('last_update'))
        engine.execute("INSERT INTO availability_data values (%s,%s,%s,%s,%s)", data_points)
        #print(data_points)

while True:
    avail_to_db()
    time.sleep(10*60)

#avail_to_db()
