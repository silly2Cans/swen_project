#! usr/bin/env python3

import requests
import json
from pprint import pprint
def get_weather():
    """Get the weather data from openweathermap.org API"""
    
    APIURL = "http://api.openweathermap.org/data/2.5/forecast"
    APIKEY = "2a2976ca391b03a9c1c9f1eba7680faa"
    CITYID = "2965768"
#     Make request and print the data
    request = requests.get(APIURL, params={'id':CITYID,'APPID':APIKEY})
#     return request.text
#     print(request.text)
    data = json.loads(request.text)
#     print(data["city"])
    return data
#     pprint(data)


weather = get_weather()
pprint(weather)
