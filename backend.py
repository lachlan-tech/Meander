# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# This Program is for frameworking the allschools website, it glues the peices together and runs from a single line of code
# In the terminal enter the following run code: python framework.py
#
# CODE COMMENTING
# (# ______________________________________________________________________________________________________________________________________________________________)
# This is a main title - A very important Branch or point of the website, including(Main webpage, TeacherHUb, StudentHub, AdminHub. Import and call point, Run point)
# (# /////////)
# This is The setup root of a main webpage branch
# (# ------------------------------------------------------------)
# This is a subpage - A webpage underneath a main branch
# (# XXXXXXXXXX)
# This is a description
#
# --------------------------------------------------------------------------------------------------------------------------------------------------------------


# ______________________________________________________________________________________________________________________________________________________________
# Import and call Point 
# ______________________________________________________________________________________________________________________________________________________________
from flask import Flask, redirect, render_template, request, session, url_for
from time import strftime, time
import pandas as pd
from statistics import mode
import requests
import mysql.connector as mysql
#from weatherdb import weather

# ______________________________________________________________________________________________________________________________________________________________
# Database Connection
# ______________________________________________________________________________________________________________________________________________________________
#db = mysql.connect(host = "localhost",user = "root",passwd = "Hole_1234",database = "allschools")
#print(db)


#get_times = ["13 : 45", "13 : 46", "13 : 47",]

#cursor = db.cursor()
#query = "INSERT INTO users (name, accesscode) VALUES (%s, %s)"
#values = ("Hafeez", "hafeez")
#cursor.execute(query, values)
#db.commit()
#print(cursor.execute("SELECT * FROM users"))

password1 = "+isi"
password2 = "uocrx"
password3 = "q'uks"
username1 = 'user'


# ______________________________________________________________________________________________________________________________________________________________
# Import and call Point 
# ______________________________________________________________________________________________________________________________________________________________

def findateacher():
    #setting date and time (redifine these to make it a permanant situation)
    search = request.form["name"]
    print(search)
    lastname = search
    date = "28/01/2021" #strftime("%d/%m/%Y")
    hour = strftime("%H")
    minute = int(strftime("%M"))
    if hour == "08":
        hour = "8"
    if hour == "09":
        hour = "9"
    print(hour)
    print(minute)
    # m1 (for later in the program)
    m1 = strftime("%M")
    period = ""
    #changing M1 manually so that the integers from the clock format correctly
    m1vals = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
    for i in range(len(m1vals)):
        if m1 == m1vals[i]:
            minute = i
    #deciding the period
    hourvals = ["8", "8", "9", "9", "10", "11", "12", "13", "14" ]
    minvals = [40, 38, 45, 45, 0, 0, 40, 0, 35]
    periodvals = ["8:30", "8:40", "8:40", "9:50", "9:50", "11:30", "11:30", "13:25", "13:25"]
    for i in range(len(hourvals)):
        if hour == hourvals[i]:
            if minute > minvals[i]:
                period = periodvals[i]
            if minute < minvals[i]:
                period = periodvals[i]
    #setting the values for room retrival 
    Date = 1
    Start_Time = 3
    Staff_Last_Name = 6
    Facility_Code = 8
    #retriving and stripping values for output
    timetable = pd.read_csv("Timetable.csv", header=None, index_col=None)
    res = timetable.loc[(timetable[Staff_Last_Name] == lastname) & (timetable[Date] == date) & (timetable[Start_Time] == period)]
    answer1 = res[Facility_Code]
    answer2 = str(answer1.values)
    resulta = answer2.strip("[']")
    result = str("In:" + resulta)
    #if no result output try again code
    if resulta == "":
        result = "Currently Out Of Class: Please Try thier Staffroom, Or Check If They Are On Lunch Duty"
    return result

# ______________________________________________________________________________________________________________________________________________________________
# The security portion of the backend this is for the login page
# ______________________________________________________________________________________________________________________________________________________________

def Security():
    password = request.form["Pass"]
    username = request.form["Uname"]

    chars = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "`", "~", "-", "_", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "/", "?", "=", "+", "\'", "\"", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m", "[", "]", "|"]
    encryptedpass = []
    for x in password:
        for i in range(len(chars)):
            if x == chars[i]:
                if i < 4:
                    newchar = chars[int(i+4)]
                    encryptedpass.append(newchar)
                if i > 4:
                    newchar = chars[int(i-4)]
                    encryptedpass.append(newchar)
    password = ''.join(encryptedpass)
    if username == username1:
        if password == password1:    
            return redirect(url_for('studentpage'))
        if password == password2:
            return redirect(url_for('adminpage'))
        if password == password3:
            return redirect(url_for('teacherpage'))
        # If incorrect stay on the password page
        return render_template("mainfiles/login.html")

# ______________________________________________________________________________________________________________________________________________________________
# Code for the traffic lights program
# ______________________________________________________________________________________________________________________________________________________________

def TrafficLights(pg):
    rank = 0
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

    #rank tempurature 
    if temp >= 16 and temp <= 35:
        rank += 1
    if temp >= 36 and temp <= 44:
        rank += 2
    if temp >= 6 and temp <= 15:
        rank += 2
    if temp >= 45:
        rank += 3
    if temp <= 5:
        rank += 3

    #rank humidity
    if humidity >= 20 and humidity <= 80:
        rank += 1
    if humidity >= 6 and humidity <= 19:
        rank += 2
    if humidity >= 81 and humidity <= 94:
        rank += 2
    if humidity >= 0 and humidity <= 5:
        rank += 3
    if humidity >= 95 and humidity <= 100:
        rank += 3

    #rank cloud percentage
    found = False
    for i in range(10):
        if found == False:
            for x in range(10):
                if found == False:
                    num = int(i * 10) + x
                    if cloud == num:
                        found = True
                if rank == 10 and cloud == 100:
                    found = True
            rank += 1

    #rank moon percentage
    found = False
    for i in range(10):
        if found == False:
            for x in range(10):
                if found == False:
                    num = int(i * 10) + x
                    if moon == num:
                        found = True
                if rank == 10 and moon == 100:
                    found = True
            rank += 1
    
    # send out data based on rankings
    if rank >= 20: #rank BLACK
        return render_template(pg, val5=url_for('static', filename='teacherpagefiles/traffic-light-black.png'), val1=temp, val2=humidity, val3=cloud, val4=moon)
    if rank >= 15 and rank <= 19: #rank RED
        return render_template(pg, val5=url_for('static', filename='teacherpagefiles/traffic-light-red.png'), val1=temp, val2=humidity, val3=cloud, val4=moon)
    if rank >= 10 and rank <= 14: #rank YELLOW
        return render_template(pg, val5=url_for('static', filename='teacherpagefiles/traffic-light-yellow.png'), val1=temp, val2=humidity, val3=cloud, val4=moon)
    if rank >= 4 and rank <= 9: #rank GREEN
        return render_template(pg, val5=url_for('static', filename='teacherpagefiles/traffic-light-green.png'), val1=temp, val2=humidity, val3=cloud, val4=moon)
