import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  password="msci342!",
  database="moviedb"
)

mycursor = mydb.cursor()

sql = "DROP TABLE testtbl;"

mycursor.execute(sql)

mydb.commit()