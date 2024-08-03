import requests
import json

response = json.load(open('key.json'))
city = str(input("Enter the name of the city you want find the weather about: "))
api_key = response["api_key"]
url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'

try:
    response = requests.get(url, verify=False).json()

    city = (response["location"]["name"])
    country = (response["location"]["country"])
    temp_c = (response["current"]["temp_c"])
    temp_f = (response["current"]["temp_f"])
    humidity = (response["current"]["humidity"])
    conditions = (response["current"]["condition"]["text"])

    print("City: " + city)
    print("Country: " + country)
    print("temp_c: " + str(temp_c) + chr(176) + "C")
    print("temp_f: " + str(temp_f) + chr(176) + "F")
    print("humidity: " + str(humidity) + "%")
    print("conditions: " + conditions)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data : {e}")
except KeyError as e:
    print(f"Error processing weather data: {e}")
