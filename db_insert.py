import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  password="msci342!",
  database="moviedb"
)

mycursor = mydb.cursor()

#sql = "CREATE TABLE usermovieblacklistvote (movieID INT NOT NULL,userID INT NOT NULL,groupID INT NOT NULL,blacklist_vote BOOLEAN,PRIMARY KEY (movieID,userID,groupID),FOREIGN KEY (movieID) REFERENCES userratesmovie(movieID),FOREIGN KEY (groupID) REFERENCES useringroup(groupID),FOREIGN KEY (userID) REFERENCES useringroup(userID));"
sql = "delete from userratesmovie;"
# sql = "drop table user_movie_blacklist_vote;"


mycursor.execute(sql)

mydb.commit()