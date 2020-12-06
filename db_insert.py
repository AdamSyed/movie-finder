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
#sql = "insert into movie (name,year,director,genre) values "
sql = "delete from usermovieblacklistvote;"
#sql = "insert into user (email,password,firstname,lastname) values"
#sql = "insert into useringroup(groupID,userID,joined_at,left_at) values (16,13,NULL,NULL),(16,14,NULL,NULL),(16,15,NULL,NULL),(16,16,NULL,NULL) "
#sql = "insert into usermovieblacklistvote(groupID,userID,movieID,blacklist_vote) values (16,13,9,1)"

mycursor.execute(sql)

mydb.commit()