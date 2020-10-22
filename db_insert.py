import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  passwd="msci342!",
  database="moviedatabase"
)

mycursor = mydb.cursor()

sql = "CREATE TABLE test_tbl (id int, name varchar(255));"

mycursor.execute(sql)

mydb.commit()