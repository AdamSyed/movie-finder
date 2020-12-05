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
#sql = "insert into grp (name,blacklist_threshold,max_size) values ('Test Group', 4, 5)"
sql = "DELETE FROM user;"


mycursor.execute(sql)

mydb.commit()