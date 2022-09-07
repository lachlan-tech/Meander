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
db = mysql.connect(host = "meander.cp7w8rn9hrdf.us-west-1.rds.amazonaws.com",port="3306",user = "admin",password = "meander.1",)
cursor = db.cursor()
# ______________________________________________________________________________________________________________________________________________________________
# Import and call Point 
# ______________________________________________________________________________________________________________________________________________________________

def findateacher():
    #setting date and time (redifine these to make it a permanant situation)
    search = request.form["name"]
    lastname = search
    date = "28/01/2021" #strftime("%d/%m/%Y")
    hour = strftime("%H")
    minute = int(strftime("%M"))
    if hour == "08":
        hour = "8"
    if hour == "09":
        hour = "9"
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
    sql = "SELECT * FROM `Meander-secure`.userdata WHERE user = %s AND password = %s"
    u = (username, password)
    cursor.execute(sql, u)
    myresult = cursor.fetchall()
    if myresult[0][3] == "1":    
        return redirect(url_for('studentpage'))
    if myresult[0][3] == "2":
        return redirect(url_for('teacherpage'))
    if myresult[0][3] == "3":
        return redirect(url_for('adminpage'))
        
    # If incorrect stay on the password page
    return render_template("mainfiles/login.html")

# ______________________________________________________________________________________________________________________________________________________________
# Code for the traffic lights program
# ______________________________________________________________________________________________________________________________________________________________

def TrafficLights():
    rank = 0
    cursor.execute("SELECT * FROM `Meander-secure`.weather")
    myresult = cursor.fetchall()
    temp = float(myresult[0][1])
    humidity = int(myresult[0][2])
    cloud = int(myresult[0][3])
    moon = int(myresult[0][4])

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
        vals = [temp, humidity, cloud, moon, url_for('static', filename='teacherpagefiles/traffic-light-black.png')]
        return vals 
    if rank >= 15 and rank <= 19: #rank RED
        vals = [temp, humidity, cloud, moon, url_for('static', filename='teacherpagefiles/traffic-light-red.png')]
        return vals 
    if rank >= 10 and rank <= 14: #rank YELLOW
        vals = [temp, humidity, cloud, moon, url_for('static', filename='teacherpagefiles/traffic-light-yellow.png')]
        return vals 
    if rank >= 4 and rank <= 9: #rank GREEN
        vals = [temp, humidity, cloud, moon, url_for('static', filename='teacherpagefiles/traffic-light-green.png')]
        return vals 
