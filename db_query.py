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
mycursor.execute("select * from usermovieblacklistvote;")
#mycursor.execute("select * from movie;")
#mycursor.execute("select * from useringroup;")
#mycursor.execute("select * from grp where groupID = 3;")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)