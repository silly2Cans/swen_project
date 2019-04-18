from pprint import pprint
import requests
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
import simplejson as simjson
import time
# from IPython.display import display
import pymysql
import main
def get_forecast():
    """Get the weather data from openweathermap.org API"""

    APIURL = "http://api.openweathermap.org/data/2.5/forecast"
    APIKEY = "2a2976ca391b03a9c1c9f1eba7680faa"
    CITYID = "2964574"
    #     Make request and print the data
    request = requests.get(APIURL, params={'id': CITYID, 'APPID': APIKEY})
    #     return request.text
    #     print(request.text)
    data = json.loads(request.text)
    #     print(data["city"])
    return data


#     pprint(data)
forecast = get_forecast()
#pprint(forecast)
list1=forecast['list']
#print(list1)
length=len(list1)
def getdict(num):
    main1=list1[num]['main']
    weather1=list1[num]['weather'][0]
    weather1['icon'] = weather1['icon'] + ".png"
    wind1=list1[num]['wind']
    wind1['windspeed'] = wind1['speed']
    del wind1['speed']
    main1.update(weather1)
    main1.update(wind1)
    main1['date']=list1[num]['dt_txt']
    return main1

# weather1=list1[2]['main']
# wind1=list1[0]['wind']
# wind1['windspeed'] = wind1['speed']
# del wind1['speed']
# weather1.update(wind1)


# DBURL = 'swen-db.cakbys7wmjxf.eu-west-1.rds.amazonaws.com'
# PORT = '3306'
# DB = 'dublin_bikes'
# USER = 'swen_main_'
# PASSWORD = 'mixednuts'
# i=0
# engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, DBURL, PORT, DB))
# print(engine)

while(i<length):
    data=getdict(i)
    data_points = (data.get('id'),data.get('date'), data.get('temp'), data.get('humidity'),
                   data.get('pressure'),data.get('description'), data.get('icon'), data.get('windspeed'))
    dat=data.get('date')
    rows = engine.execute("SELECT COUNT(*) from weatherforecasting where date ="+dat+";")
    i = i + 1
    if rows!=0:
        print("The record at this time is already in the database")
        continue
    else:
        engine.execute("INSERT INTO weatherforecasting values (%s,%s,%s,%s,%s,%s,%s,%s)", data_points)
    #         print(data_points)
    #         print("%s,%s,%s,%s,%s,%s" % data_points)

engine.dispose()










