import mysql.connector

mydb = mysql.connector.connect(
  host="moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com",
  port=3306,
  user="admin",
  password="msci342!",
  database="moviedb"
)

mycursor = mydb.cursor()

<<<<<<< HEAD
sql = "CREATE TABLE userratesmovie(movieID INT,userID INT,isLiked BOOLEAN, PRIMARY KEY (movieID,userID),FOREIGN KEY (movieID) REFERENCES movie(movieID),FOREIGN KEY (userID) REFERENCES user(userID));"
# sql = "drop table user_rates_movie;"
# sql = "drop table user_movie_blacklist_vote;"


=======
#sql = "Insert into movie (name, year, director, imdb_rating, genre) values ('The Proposal','2009','Anne Fletcher',6.7, 'Romance'),('Inception',2010,'Christopher Nolan', 8.8, 'Action'),('Knives Out',2019,'Rian Johnson', 7.9, 'Comedy')"
sql = "Insert into userratesmovie (movieID, userID, isLiked) values (8,1,False)"
#sql= "Insert into genres(genre) values ('Action'),('Adventure'),('Animation'),('Biography'),('Comedy'),('Crime'),('Documentary'),('Drama'),('Family'),('Fantasy'),('Film Noir'),('History'),('HorrorMusic'),('Musical'),('Mystery'),('Romance'),('Sci-Fi'),('Short Film'),('Sport'),('Superhero'),('Thriller'),('War'),('Western')"
>>>>>>> main
mycursor.execute(sql)

mydb.commit()