from flask import Flask
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

# Initiate Student Schema
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

# class user_rates_movie(db.Model):


@application.route('/', methods=['GET'])
def default():
    u = User.query.filter_by(userID=1).first()
    return {'Does this work?':u.userID}

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

# Run server
if __name__ == '__main__':
    # application.run(host='0.0.0.0')
    application.run(debug=True)