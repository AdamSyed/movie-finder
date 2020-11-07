from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import numpy as np

# Initiate application
application = Flask(__name__)

# Database
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:msci342!@moviedatabase.cabnbngmbcmp.ca-central-1.rds.amazonaws.com:3306/moviedb'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To prevent any complaints in console

# Initialize DB
db = SQLAlchemy(application)

# Initialize marshmallow
ma = Marshmallow(application)

# Classes, constructors, schemas & initiate
# User Class
class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    moviesRated = db.relationship('Userratesmovie', backref='user', lazy=True)
    groups = db.relationship('Useringroup', backref='user', lazy=True)
    movieblacklistedvotes = db.relationship('Usermovieblacklistvote', backref='user', lazy=True)

    def __init__(self,email,password,firstname,lastname):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

# User Schema - for marshmallow
class UserSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('userID','email','password','firstname','lastname')

# Initiate User Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Actor Class
class Actor(db.Model):
    actorID = db.Column(db.Integer, primary_key=True)
    actor_firstname = db.Column(db.String(100), nullable=False)
    actor_lastname = db.Column(db.String(200), nullable=False)
    movies = db.relationship('Actorinmovie', backref='actor', lazy=True)
    
    def __init__(self,actorID,actor_firstname,actor_lastname):
        self.actorID = actorID
        self.actor_firstname = actor_firstname
        self.actor_lastname = actor_lastname

# Actor Schema - for marshmallow
class ActorSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('actorID','actor_firstname','actor_lastname')

# Initiate Actor Schema
actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)

# Group Class
class Grp(db.Model):
    groupID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    blacklist_threshold = db.Column(db.Integer)
    max_size = db.Column(db.Integer)
    users = db.relationship('Useringroup', backref='grp', lazy=True)
    userblacklistvotes =  db.relationship('Usermovieblacklistvote', backref='grp', lazy=True)

    def __init__(self,groupID,name,blacklist_threshold,max_size):
        self.groupID = groupID
        self.name = name
        self.blacklist_threshold = blacklist_threshold
        self.max_size = max_size

# Group Schema - for marshmallow
class GrpSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('groupID','name','blacklist_threshold','max_size')

# Initiate Group Schema
grp_schema = GrpSchema()
grps_schema = GrpSchema(many=True)

# Movie Class
class Movie(db.Model):
    movieID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    director = db.Column(db.String(200))
    genre = db.Column(db.String(200))
    imdb_rating = db.Column(db.Float)
    photo = db.Column(db.String(500))
    imdb_link = db.Column(db.String(500))
    moviesRated = db.relationship('Userratesmovie', backref='movie', lazy=True)
    actors = db.relationship('Actorinmovie', backref='movie', lazy=True)
    userblacklistvotes = db.relationship('Usermovieblacklistvote', backref='movie', lazy=True)

    def __init__(self,movieID,name,year,director,genre,imdb_rating,photo,imdb_link):
        self.movieID = movieID
        self.name = name
        self.year = year
        self.director = director
        self.genre = genre
        self.imdb_rating = imdb_rating
        self.photo = photo
        self.imdb_link = imdb_link

# Movie Schema - for marshmallow
class MovieSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('movieID','name','year','director','genre','imdb_rating','photo','imdb_link')

# Initiate Movie Schema
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class Userratesmovie(db.Model):
    movieID = db.Column (db.Integer, db.ForeignKey(Movie.movieID),primary_key=True)
    userID = db.Column (db.Integer, db.ForeignKey(User.userID),primary_key=True)
    isLiked = db.Column (db.Boolean, nullable = False)

    def __init__(self,movieID,userID,isLiked):
        self.movieID = movieID
        self.userID = userID
        self.isLiked = isLiked

# User_rates_Movie Schema - for marshmallow
class UserRatesMovieSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('movieID','userID','isLiked')

# Initiate User_Rates_Movie Schema
userRatesMovie_schema = UserRatesMovieSchema()
userRatesMovies_schema = UserRatesMovieSchema(many=True)

# UserInGroup Class
class Useringroup(db.Model):
    groupID = db.Column (db.Integer, db.ForeignKey(Grp.groupID),primary_key=True)
    userID = db.Column (db.Integer, db.ForeignKey(User.userID),primary_key=True)
    joined_at = db.Column(db.DateTime)
    left_at = db.Column (db.DateTime)

    def __init__(self,groupID,userID,joined_at,left_at):
        self.groupID = groupID
        self.userID = userID
        self.joined_at = joined_at
        self.left_at = left_at

# UserInGroupSchema Schema - for marshmallow
class UserInGroupSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('groupID','userID','joined_at','left_at')

# Initiate UserInGroupSchema Schema
userInGroup_schema = UserInGroupSchema()
userInGroups_schema = UserInGroupSchema(many=True)

# Actorinmovie Class
class Actorinmovie(db.Model):
    movieID = db.Column (db.Integer, db.ForeignKey(Movie.movieID),primary_key=True)
    actorID = db.Column (db.Integer, db.ForeignKey(Actor.actorID),primary_key=True)
    
    def __init__(self,movieID,actorID):
        self.movieID = movieID
        self.actorID = actorID
    
# Actorinmovie Schema - for marshmallow
class ActorInMovieSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('movieID','actorID')

# Initiate Actorinmovie Schema
ActorInMovie_schema = ActorInMovieSchema()
ActorInMovies_schema = ActorInMovieSchema(many=True)

# UserMovieBlacklistVote Class
class Usermovieblacklistvote(db.Model):
    movieID = db.Column (db.Integer, db.ForeignKey(Movie.movieID),primary_key=True)
    userID = db.Column (db.Integer, db.ForeignKey(User.userID),primary_key=True)
    groupID = db.Column (db.Integer, db.ForeignKey(Grp.groupID),primary_key=True)
    blacklist_vote = db.Column (db.Boolean)
    
    def __init__(self,movieID,userID,groupID,blacklist_vote):
        self.movieID = movieID
        self.userID = userID
        self.groupID = groupID
        self.blacklist_vote = blacklist_vote
    
# UserMovieBlacklistVote Schema - for marshmallow
class UserMovieBlacklistVoteSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('movieID','userID','groupID','blacklist_vote')

# Initiate UserMovieBlacklistVote Schema
UserMovieBlacklistVote_schema = UserMovieBlacklistVoteSchema()
UserMovieBlacklistVotes_schema = UserMovieBlacklistVoteSchema(many=True)

@application.route('/', methods=['GET'])
def default():
    return {'Does this work?':'Yes'}

# ENDPOINT - Login
@application.route('/login', methods=['POST'])
def check_login_creds():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email, password=password).first()

    if bool(user) == True:
        output = {"response": str(user.userID)}
    else:
        output = {"response": "Invalid credentials."}

    return jsonify(output)

# ENDPOINT - Create user account
@application.route('/create',methods=['PUT'])
def create():
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']
    
    user = User(email,password,first_name,last_name)

    db.session.add(user)
    db.session.commit()

    user_id = User.query.filter_by(email = email).first().userID
    output = {'response':user_id}

    return jsonify(output)

# ENDPOINT - Get user preferences
@application.route('/user-preferences',methods=['POST'])
def user_preferences():
    id = request.json['id']
    
    user = User.query.filter_by(userID=id).first()

    if bool(user) == True:
        output = {"email":user.email, "password":user.password,"firstname":user.firstname,"lastname":user.lastname}
    else:
        output = {"response": "Invalid ID."}

    return jsonify(output)

# ENDPOINT - Update user preferences
@application.route('/update-user-preferences',methods=['PUT'])
def update_user_preferences():
    id = request.json['id']
    user = User.query.get(id)

    user.firstname = request.json['firstname']
    user.lastname = request.json['lastname']
    user.password = request.json['password']

    try:
        db.session.commit()
        output = {'response':'Success'}
    except:
        output = {'response':'Error'}

    return jsonify(output)

# ENDPOINT - Get all movie rated by a user
@application.route('/all-movie-ratings',methods=['POST'])
def all_movie_ratings():
    id = request.json['id']
    
    user = User.query.filter_by(userID=id).first()

    if bool(user) == True:
        output = []
        for m in user.moviesRated:
            movie = Movie.query.filter_by(movieID = m.movieID).first()
            output.append({'movieName':movie.name,'isLiked':m.isLiked})
    else:
        output = {"response": "Invalid ID."}

    return jsonify(output)

@application.route('/rating', methods = ['POST'])
def movie_option():
    userID = request.json['id']

    #this endpoint will take the user id and look through all the movies in the database that do not have a Yes/No choice made already by the user
    #it will then output one of those undecided options for the movie

    #first query to get the user that is currently logged in
    m = User.query.filter_by(userID=userID).first()
    
    #logic for finding a movie
    #1. Get a list of all rated movies for a user and we convert this into a list of movieIds only
    
    #declare list variable to add movieIDs to
    ratedMovies = []
    
    #2. For each movie-user-rated relationship, we append the movieID to out list of ratedMovies
    for i in m.moviesRated:
        ratedMovies.append(i.movieID)

    #3. Get a list of all the movies
    allMovieID = []
    allMovies = Movie.query.all()
    for j in allMovies:
        allMovieID.append(j.movieID)

    #4. Find the movies that are in the list of all movies but not in the list of the movies rated by the user (this can be done by comparing the 2 lists)
    unratedMovies = np.setdiff1d(allMovieID,ratedMovies)

    #5. Gather the relevant details of the first movie on that list from 4 to output
    #right now we use a simple selection of the first movie on the list.  Later on, if we feel that more complex logic is needed to create a fair representation, then that can be changed below
    #add in a try/except in case all movies have been rated
    try:
        nextMovie = Movie.query.get(unratedMovies[0])
        movieData = [userID, nextMovie.movieID, nextMovie.name, nextMovie.genre, nextMovie.director]
    except:
        movieData = [userID, 'N/A', 'N/A', 'N/A', 'N/A']
    
    #finally, we return the results
    return jsonify(movieData)


# # ENDPOINT - User rating yes
# @application.route('/rate-yes', methods = ['PUT'])
# def rate_yes():
#     movieID = request.json['movieID']
#     userID = request.json['userID']
    
#     user_rates_movie_schema = User_Rates_Movie(movieID,userID,True)

#     db.session.add(user_rates_movie_schema)
#     db.session.commit()
#     # call method to display movie, will display a new unseen movie

#     return ({'response':'Good'})
#     # this method will insert into the user_rates_movie table 

# # ENDPOINT - User rating no
# @application.route('/rate-no', methods = ['PUT'])
# def rate_yes():
#     movieID = request.json['movieID']
#     userID = request.json['userID']
    
#     user_rates_movie_schema = User_Rates_Movie(movieID,userID,False)

#     db.session.add(user_rates_movie_schema)
#     db.session.commit()
#     # call method to display movie, will display a new unseen movie

#     return ({'response':'Good'})
#     # this method will insert into the user_rates_movie table 


# Run server
if __name__ == '__main__':

    #application.run(host='0.0.0.0')
    application.run(debug=True)