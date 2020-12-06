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
#mycursor.execute("select * from useringroup;")

#mycursor.execute("select * from usermovieblacklistvote where userID = 15;")
mycursor.execute("select * from information_schema.tables';")
#mycursor.execute("select * from grp;")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)