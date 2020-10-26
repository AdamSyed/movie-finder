from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

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


@application.route('/rating/<userID>', methods = ['GET'])
def movie_option(userID):
    #this endpoint will take the user id and look through all the movies in the database that do not have a Yes/No choice made already by the user
    #it will then output one of those undecided options for the movie

    #first query to get the user that is currenlty logged in
    m = User.query.filter_by(userID=userID).first()
    
    #this needs to be expanded in future sprints

    #the results scanner is hardcoded for Sprint 1 to take in the first instace in the User_Rates_Movies index to see if the user has any movies they have alreadty watched
    results = [m.moviesRated[1].movieID, m.moviesRated[1].userID, m.moviesRated[1].isLiked]

    #next, we get movies that are not on the list to get the movies that have not been rated
    moviesUnrated = Movie.query.filter(Movie.movieID != results[0]).first()
    movieData = [moviesUnrated.name, moviesUnrated.genre]

    #finally, return the data of the movie being rated, the userID, and the movie info to display
    fullResults = [results[0],results[1],movieData[0],movieData[1]]

    #next 2 lines are for unit testing of the arrays that we will send to the JS
    #print (results)
    #print (movieData)
   
    return jsonify(fullResults)

# ENDPOINT - User rating
@application.route('/rate-yes', methods = ['PUT'])
def rate_yes():
    movieID = request.json['movieID']
    userID = request.json['userID']
    
    user_rates_movie_schema = User_Rates_Movie(movieID,userID,True)

    db.session.add(user_rates_movie_schema)
    db.session.commit()

    return ({'response':'Good'})
    # this method will insert into the user_rates_movie table 

# Run server
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)