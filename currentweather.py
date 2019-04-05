import requests
import json

def get_weather():
    """Get the weather data from openweathermap.org API"""
    #     Do not make more than 60 requests per hour.

    APIURL = "http://api.openweathermap.org/data/2.5/weather"
    APIKEY = "2a2976ca391b03a9c1c9f1eba7680faa"
    CITYID = "2964574"
    #     Make request and print the data
    request = requests.get(APIURL, params={'id': CITYID, 'APPID': APIKEY})
    #     return request.text
    #     print(request.text)
    data = json.loads(request.text)
    # print(data["name"])
    return data


def currentWeather():
    weather = get_weather()
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
    # dd1=json.loads(dd1)
    # print(dd1)
    # print(type(dd1))
    return dd1
currentWeather()




