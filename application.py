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

# XXXXXXXXXX
# This Section imports all of the required libraries for the code it also adds in the backend code link (see backend.py)
# XXXXXXXXXX

from flask import Flask, redirect, render_template, request, session, url_for
from backend import Security, TrafficLights, findateacher

# XXXXXXXXXX
# This Section calls the variable app, this holds all of the routing information for the website.
# XXXXXXXXXX

app = Flask(__name__)

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

# ------------------------------------------------------------
# Setting up a subpage for the teacher content pack register page
# ------------------------------------------------------------
@app.route('/teachercontentpack')
def teachercontentpackdesc():
    return render_template("mainfiles/teachercontentpack.html",)

# ------------------------------------------------------------
# Setting up a subpage for the student content pack register page
# ------------------------------------------------------------
@app.route('/studentcontentpack')
def studentcontentpackdesc():
    return render_template("mainfiles/studentcontentpack.html",)

# ------------------------------------------------------------
# Setting up a subpage for the duluxe content pack register page
# ------------------------------------------------------------
@app.route('/duluxepack')
def duluxepackdesc():
    return render_template("mainfiles/duluxepack.html",)

# ------------------------------------------------------------
# Setting up a subpage for the login page
# ------------------------------------------------------------
@app.route('/login')
def login():
    return render_template("mainfiles/login.html",)
# Checking the password
@app.route('/login', methods=["POST"])
def password_check():
    return Security()  






# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the TeacherHub extension
# ______________________________________________________________________________________________________________________________________________________________

# /////////
# Setting up a root page for the TeacherHub extension
# /////////

@app.route('/teacherhub')
def teacherpage():
    return TrafficLights("teacherpagefiles/teacherpage.html")

# ------------------------------------------------------------
# The following code is for the TeacherHub's Timetable change Notification extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/teacherhub/timetablechanges')
def teachernotifications():
    return render_template("teacherpagefiles/teachertimetable.html")


# ------------------------------------------------------------
# The following code is for the TeacherHub's Planner extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/teacherhub/planner')
def teacherplanner():
    return render_template("teacherpagefiles/teacherplanner.html")


# ------------------------------------------------------------
# The following code is for the TeacherHub's Traffic light extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/teacherhub/trafficlights')
def trafficlights():
    return TrafficLights()
# ------------------------------------------------------------
# The following code is for the TeacherHub's Teacher finder extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/teacherhub/teacherfinder')
def page1():
    return render_template("teacherpagefiles/teacherfinderfiles/index.html")
# Setting up the backend
@app.route('/teacherhub/teacherfinder', methods=["POST"])
def search1():
    return render_template("teacherpagefiles/teacherfinderfiles/answer.html", value1=findateacher())

# ------------------------------------------------------------
# The following code is for the TeacherHub's Traffic light extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/teacherhub/pb4lpointsys')
def pb4lpointsys():
    return render_template("teacherpagefiles/teacherplanner.html")

# ------------------------------------------------------------
# The following code is for the TeacherHub's Traffic light extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/teacherhub/qcaatracker')
def qcaatracker():
    return render_template("teacherpagefiles/qcaatracker.html")






# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the StudentHub extension
# ______________________________________________________________________________________________________________________________________________________________

# /////////
# Setting up a root page for the StudentHub extension
# /////////

@app.route('/studenthub')
def studentpage():
    return TrafficLights("studentpagefiles/studentpage.html")

# ------------------------------------------------------------
# The following code is for the StudentHub's Timetable change Notification extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/studenthub/timetablechanges')
def studentnotifications():
    return render_template("studentpagefiles/studenttimetable.html")

# ------------------------------------------------------------
# The following code is for the StudentHub's Planner extension
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX

@app.route('/studenthub/planner')
def studentplanner():
    return render_template("studentpagefiles/studentplanner.html")

# ------------------------------------------------------------
# The following code is for the StudentHub's Teacher finder extension
# ------------------------------------------------------------
@app.route('/studenthub/teacherfinder')
def page2():
    return render_template("studentpagefiles/teacherfinderfiles/index.html")
# Setting up the backend
@app.route('/studenthub/teacherfinder', methods=["POST"])
def search2():
    return render_template("studentpagefiles/teacherfinderfiles/answer.html", value1=findateacher())






# ______________________________________________________________________________________________________________________________________________________________
# The following code is for the AdminHub extension
# ______________________________________________________________________________________________________________________________________________________________

# /////////
# Setting up a root page for the AdminHub extension
# /////////

@app.route('/adminpage')
def adminpage():
    return render_template("adminpagefiles/adminpage.html",)

# ------------------------------------------------------------
# The following code is for the 
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX



# ------------------------------------------------------------
# The following code is for the 
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX



# ------------------------------------------------------------
# The following code is for the 
# ------------------------------------------------------------

# XXXXXXXXXX
# The backend code for this extension can be found in the backend.py file
# XXXXXXXXXX



# ------------------------------------------------------------
# The following code is for the 
# ------------------------------------------------------------

# XXXXXXXXXX
# This Section calls the variable app, this holds all of the routing information for the website.
# XXXXXXXXXX















# ______________________________________________________________________________________________________________________________________________________________
# Run the app
# ______________________________________________________________________________________________________________________________________________________________

#if __name__ == '__main__':
#    app.run()