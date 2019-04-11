#!usr/bin/env python3

# env includes
import requests
# part of Python standard library
import json



# Define the URL and make the request using the API (incl key)
url= "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=7b9a350297fefef5f4147e65b6bc3114aacde014"
jsonText = requests.get(url).text

# Create a json file to hold the intermediate data
with open("text.json", 'w') as fout:
    fout.write(jsonText)

# Handle the json data from the open file
jsonData = json.load(open('text.json', 'r'))

# Render the data from the file
for i in jsonData:
    freeBikes = i["bike_stands"] - i["available_bike_stands"]
    print(i["name"], 
          "\n", 
          "Bike Stands:", 
          i["bike_stands"], 
          "\n", 
          "Stands Available:", 
          i["available_bike_stands"],
          "\n",
          "Free Bikes:",
          freeBikes,
          end="\n\n")




    

    
    

