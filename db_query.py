import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  password="msci342!",
  database="moviedb"
)

mycursor = mydb.cursor()

#mycursor.execute("select * from userratesmovie where userID=2;")
#mycursor.execute("select * from userratesmovie where userID=6;")
mycursor.execute("select * from grp;")
#mycursor.execute("select * from useringroup;")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)