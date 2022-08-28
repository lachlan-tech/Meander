import time
import requests
import mysql.connector as mysql

db = mysql.connect(host = "localhost",user = "root",passwd = "Hole_1234",database = "allschools")
print(db)
cursor = db.cursor()
query = "INSERT INTO users (name, accesscode) VALUES (%s, %s)"
values = ("Hafeez", "hafeez")
cursor.execute(query, values)
db.commit()
print(cursor.execute("SELECT * FROM users"))

# On initial run, update weather to be called will auto sync at the next update, to ensure there are no crashes, and we keep the number of calls in check.
url = "https://weatherapi-com.p.rapidapi.com/current.json"
querystring = {"q":"Brisbane"}
headers = {"X-RapidAPI-Key": "574c319c1bmshbd3b1d2aceffbc4p148f2bjsn618e60f3d821", "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
response = requests.request("GET", url, headers=headers, params=querystring)
data1raw = response.json()
data1 = data1raw["current"]
url = "https://weatherapi-com.p.rapidapi.com/astronomy.json"
querystring = {"q":"Brisbane"}
headers = {"X-RapidAPI-Key": "574c319c1bmshbd3b1d2aceffbc4p148f2bjsn618e60f3d821","X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
response = requests.request("GET", url, headers=headers, params=querystring)
data2raw1 = response.json()
data2raw2 = data2raw1["astronomy"]
data2 = data2raw2["astro"]
temp = data1["temp_c"]
humidity = data1["humidity"]
cloud = data1["cloud"]
moon = data2["moon_illumination"]
weather = [temp, humidity, cloud, moon]

while True:
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q":"Brisbane"}
    headers = {"X-RapidAPI-Key": "574c319c1bmshbd3b1d2aceffbc4p148f2bjsn618e60f3d821", "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data1raw = response.json()
    data1 = data1raw["current"]
    url = "https://weatherapi-com.p.rapidapi.com/astronomy.json"
    querystring = {"q":"Brisbane"}
    headers = {"X-RapidAPI-Key": "574c319c1bmshbd3b1d2aceffbc4p148f2bjsn618e60f3d821","X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data2raw1 = response.json()
    data2raw2 = data2raw1["astronomy"]
    data2 = data2raw2["astro"]
    temp = data1["temp_c"]
    humidity = data1["humidity"]
    cloud = data1["cloud"]
    moon = data2["moon_illumination"]
    weather = []
    weather.append(temp)
    weather.append(humidity)
    weather.append(cloud)
    weather.append(moon)
    print("Weather has been updated:", weather)
    time.sleep(10)