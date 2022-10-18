# ______________________________________________________________________________________________________________________________________________________________
# Import and call Point 
# ______________________________________________________________________________________________________________________________________________________________
from flask import Flask, redirect, render_template, request, session, url_for
from time import strftime, time
import pandas as pd
from statistics import mode
import requests
import mysql.connector as mysql
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "fc984a82b358333ca0320887c30dc407"

db = mysql.connect(host = "meander.cp7w8rn9hrdf.us-west-1.rds.amazonaws.com",port="3306",user = "admin",password = "meander.1")
cursor = db.cursor()

# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the main welcome website
# ______________________________________________________________________________________________________________________________________________________________
# /////////
# Seting up the root landing page for the main website
# /////////
@app.route('/')
def index():
    return render_template("index.html",)

# ------------------------------------------------------------
# Setting up a subpage for the teacher finder project page
# ------------------------------------------------------------
@app.route('/teacherfinder')
def teacherfinderdesc():
    return render_template("mainfiles/teacherfinder.html",)
# ------------------------------------------------------------
# Setting up a subpage for the student notification project page
# ------------------------------------------------------------
@app.route('/studentnotifications')
def studentnotificationsdesc():
    return render_template("mainfiles/studentnotifications.html",)
# ------------------------------------------------------------
# Setting up a subpage for the student planner project page
# ------------------------------------------------------------
@app.route('/studentplanner')
def studentplannerdesc():
    return render_template("mainfiles/studentplanner.html",)
# ------------------------------------------------------------
# Setting up a subpage for the teacher notifications project page
# ------------------------------------------------------------
@app.route('/teachernotifications')
def teachernotificationsdesc():
    return render_template("mainfiles/teachernotifications.html",)
# ------------------------------------------------------------
# Setting up a subpage for the traffic light project page
# ------------------------------------------------------------
@app.route('/trafficlightsystem')
def trafficlightsystemdesc():
    return render_template("mainfiles/trafficlightsystem.html",)



# ______________________________________________________________________________________________________________________________________________________________
# The security portion
# ______________________________________________________________________________________________________________________________________________________________
# ------------------------------------------------------------
# Setting up a subpage for the teacher content pack register page
# ------------------------------------------------------------
@app.route('/teachercontentpack')
def teachercontentpackdesc():
    return render_template("mainfiles/teachercontentpack.html",)
@app.route('/studentcontentpack')
def studentcontentpackdesc():
    return render_template("mainfiles/studentcontentpack.html",)
@app.route('/duluxepack')
def duluxepackdesc():
    return render_template("mainfiles/duluxepack.html",)

# ------------------------------------------------------------
# Setting up a subpage for the login page
# ------------------------------------------------------------ 
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        accesscode = request.form.get("accesscode")
        sql = "SELECT * FROM `Meander-secure`.User WHERE accesscode = %s AND username = %s"
        u = (accesscode, username)
        cursor.execute(sql, u)
        myresult = cursor.fetchall()
        db.commit()
        if bcrypt.check_password_hash(myresult[0][2].encode("utf-8"), password):
            if myresult[0][3] == "1":
                session['logged_in'] = True
                session['lvl'] = 1
                session['username'] = username
                return redirect(url_for('studentpage'))
            if myresult[0][3] == "2":
                session['loggedin'] = True
                session['lvl'] = 2
                session['username'] = username
                return redirect(url_for('teacherpage'))
            if myresult[0][3] == "3":
                session['loggedin'] = True
                session['lvl'] = 3
                session['username'] = username
                return redirect(url_for('adminpage'))
        else:
            # If incorrect stay on the password page
            return render_template("mainfiles/login.html")
    if request.method == "GET":
        return render_template("mainfiles/login.html")




# ______________________________________________________________________________________________________________________________________________________________
# Code for the teacher finder and traffic lights programs used in both teacherhub and studenthub
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

def TrafficLights():
    rank = 0
    cursor.execute("SELECT * FROM `Meander-secure`.weather")
    myresult = cursor.fetchall()
    db.commit()
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


# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the TeacherHub extension
# ______________________________________________________________________________________________________________________________________________________________
# /////////
# Setting up a root page for the TeacherHub extension
# /////////


@app.route('/teacherhub')
def teacherpage():
    if "logged_in" in session:
        if "lvl" in session == 2:
            return render_template("teacherpagefiles/teacherpage.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# ------------------------------------------------------------
# The following code is for the TeacherHub's Timetable change Notification extension
# ------------------------------------------------------------
@app.route('/teacherhub/timetablechanges')
def teachernotifications():
    if "logged_in" in session:
        if "lvl" in session == 2:
            return render_template("teacherpagefiles/teachertimetable.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# ------------------------------------------------------------
# The following code is for the TeacherHub's Planner extension
# ------------------------------------------------------------
@app.route('/teacherhub/planner')
def teacherplanner():
    if "logged_in" in session:
        if "lvl" in session == 2:
            return render_template("teacherpagefiles/teacherplanner.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

# ------------------------------------------------------------
# The following code is for the TeacherHub's Teacher finder extension
# ------------------------------------------------------------
@app.route('/teacherhub/teacherfinder', methods=["GET", "POST"])
def page1():
    if request.method == 'POST':
        if "logged_in" in session:
            if "lvl" in session == 2:
                return render_template("teacherpagefiles/answer.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4], value1=findateacher())
            else:
                    return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    else:
        if "logged_in" in session:
            if "lvl" in session == 2:
                return render_template("teacherpagefiles/index.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    
# ------------------------------------------------------------
# The following code is for the TeacherHub's Traffic light extension
# ------------------------------------------------------------
@app.route('/teacherhub/pb4lpointsys')
def pb4lpointsys():
    if "logged_in" in session:
        if "lvl" in session == 2:
            return render_template("teacherpagefiles/teacherplanner.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
# ------------------------------------------------------------
# The following code is for the TeacherHub's Traffic light extension
# ------------------------------------------------------------
@app.route('/teacherhub/qcaatracker')
def qcaatracker():
    if "logged_in" in session:
        if "lvl" in session == 2:
            return render_template("teacherpagefiles/qcaatracker.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))





# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the StudentHub extension
# ______________________________________________________________________________________________________________________________________________________________
# /////////
# Setting up a root page for the StudentHub extension
# /////////

@app.route('/studenthub')
def studentpage():
    if "logged_in" in session:
        if session["lvl"] == 1:
            return render_template("studentpagefiles/studentpage.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
# ------------------------------------------------------------
# The following code is for the StudentHub's Timetable change Notification extension
# ------------------------------------------------------------
@app.route('/studenthub/timetablechanges')
def studentnotifications():
    if "logged_in" in session:
        if session["lvl"] == 1:
            return render_template("studentpagefiles/studenttimetable.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
# ------------------------------------------------------------
# The following code is for the StudentHub's Planner extension
# ------------------------------------------------------------
@app.route('/studenthub/planner')
def studentplanner():
    if "logged_in" in session:
        if session["lvl"] == 1:
            return render_template("studentpagefiles/studentplanner.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
# ------------------------------------------------------------
# The following code is for the StudentHub's Teacher finder extension
# ------------------------------------------------------------
@app.route('/studenthub/teacherfinder')
def page2():
    if request.method == 'POST':
        if "logged_in" in session:
            if session["lvl"] == 1:
                return render_template("studentpagefiles/answer.html", value1=findateacher(), val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        if "logged_in" in session:
            if session["lvl"] == 1:
                return render_template("studentpagefiles/index.html", val1=TrafficLights()[0], val2=TrafficLights()[1], val3=TrafficLights()[2], val4=TrafficLights()[3], val5=TrafficLights()[4])
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))




# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the AdminHub extension
# ______________________________________________________________________________________________________________________________________________________________
# /////////
# Setting up a root page for the AdminHub extension
# /////////

@app.route('/adminpage')
def adminpage():
    if "logged_in" in session:
        if session["lvl"] == 3:
            return render_template("adminpagefiles/adminpage.html",)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



# ______________________________________________________________________________________________________________________________________________________________
# Run the app, comment out for wsgi. uncomment for local testing
# ______________________________________________________________________________________________________________________________________________________________
#if __name__ == '__main__':
#    app.run()