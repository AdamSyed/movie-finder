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
sql = "insert into useringroup (groupID,userID,joined_at,left_at) values (1, 4, NULL, NULL)"
#sql = "drop from useringroup;"


mycursor.execute(sql)

mydb.commit()