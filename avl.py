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
# from IPython.display import display
import pymysql
import csv

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
    print(tm)
    # request = requests.get(STATIONS, params={'contract':CONTRACT,'apiKey':APIKEY})
    # availability = json.loads(request.text)
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, DBURL, PORT, DB))
    with open('C:/Users/Archie/Desktop/stations.csv', mode='r') as infile:
        reader = csv.reader(infile)
        with open('stations.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            address = []
            available_bike_stands = []
            available_bikes = []
            bike_stands = []
            for rows in reader:
                data_points = (rows[9], rows[2], rows[1],rows[7],int(rows[9]*2),int(tm))
                engine.execute("INSERT INTO availability2 values (%s,%s,%s,%s,%s,%s)", data_points)
#         print(data_points)
#         print("%s,%s,%s,%s,%s,%s" % data_points)
            engine.dispose()

# while True:
#     avail_to_db()
#     time.sleep(5*60)

avail_to_db()
