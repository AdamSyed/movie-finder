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
    #moviesRated = db.relationship("Movie", secondary = "ratings")

    def __init__(self,userID,email,password,firstname,lastname):
        self.userID = userID
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
group_schema = GrpSchema()
groups_schema = GrpSchema(many=True)

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
    #moviesRated = db.relationship("User", secondary = "ratings")

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


class Userratesmovie(db.Model): ##
    movieID = db.Column (db.Integer, db.ForeignKey(Movie.movieID),primary_key=True)
    userID = db.Column (db.Integer, db.ForeignKey(User.userID),primary_key=True)
    isLiked = db.Column (db.Boolean, nullable = False)

    #user = db.relationship(User, backref=db.backref("ratings", cascade="all, delete-orphan"))
    #movie = db.relationship (Movie, backref=db.backref("ratings", cascade="all, delete-orphan"))

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
        output = {"response": str(User.userID)}
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
    
    user = User(email,first_name,last_name,password)

    db.session.add(user)
    db.session.commit()

    user_id = User.query.filter_by(email = email).first().user_ID
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


# Run server
if __name__ == '__main__':
    #application.run(host='0.0.0.0') 
    application.run(debug=True)


