import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  password="msci342!",
  database="moviedb"
)

mycursor = mydb.cursor()

<<<<<<< HEAD
mycursor.execute("select * from userratesmovie;")
=======
mycursor.execute("select * from userratesmovie")
>>>>>>> main

myresult = mycursor.fetchall()

for x in myresult:
  print(x)