import mysql.connector as mysql
db = mysql.connect(host = "localhost",user = "root",passwd = "Hole_1234",database = "allschools")
print(db)
cursor = db.cursor()
print(cursor.execute("DESC users"))
