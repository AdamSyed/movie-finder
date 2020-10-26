import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  password="msci342!",
  database="moviedb"
)

mycursor = mydb.cursor()

sql = "CREATE TABLE userratesmovie(movieID INT,userID INT,isLiked BOOLEAN, PRIMARY KEY (movieID,userID),FOREIGN KEY (movieID) REFERENCES movie(movieID),FOREIGN KEY (userID) REFERENCES user(userID));"
# sql = "drop table user_rates_movie;"
# sql = "drop table user_movie_blacklist_vote;"


mycursor.execute(sql)

mydb.commit()