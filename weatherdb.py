import time
import requests
import mysql.connector as mysql


while True:
    #DB Conn
    db = mysql.connect(host = "meander.cp7w8rn9hrdf.us-west-1.rds.amazonaws.com",port="3306",user = "admin",password = "meander.1",)
    cursor = db.cursor()
    #calling the api and getting data
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
    #send values to DB
    cursor.execute("DELETE FROM `Meander-secure`.weather")
    sql = "INSERT INTO `Meander-secure`.weather VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(sql, (1,temp,humidity,cloud,moon))
    db.commit()
    #log that the data has been updated 
    print("weather updated", temp,humidity,cloud,moon)
    #wait 5 minutes before re logging
    time.sleep(300)