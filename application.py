from flask import Flask,request, jsonify
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
    moviesRated = db.relationship('User_Rates_Movie', backref='user', lazy=True)

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
    moviesRated = db.relationship('User_Rates_Movie', backref='movie', lazy=True)

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


class User_Rates_Movie(db.Model): ##
    movieID = db.Column (db.Integer, db.ForeignKey(Movie.movieID),primary_key=True)
    userID = db.Column (db.Integer, db.ForeignKey(User.userID),primary_key=True)
    isLIked = db.Column (db.Boolean, nullable = False)

    def __init__(self,movieID,userID,isLiked):
        self.movieID = movieID
        self.userID = userID
        self.isLikeds = isLiked

# User_rates_Movie Schema - for marshmallow
class User_Rates_MovieSchema(ma.Schema):
    class Meta: #all the variables you want to see
        strict = True
        fields = ('movieID','userID','isLiked')

# Initiate User_Rates_Movie Schema
user_rates_movie_schema = User_Rates_MovieSchema()
user_rates_movies_schema = User_Rates_MovieSchema(many=True)

# # User In Group Class
# class UserGroup(db.Model):
#     groupID = db.Column(db.Integer, primary_key=True)
#     userID = db.Column(db.String(200), nullable=False)
#     joined_at = db.Column(db.Integer)
#     left_at = db.Column(db.String(200))

#     def __init__(self,movieID,name,year,director):
#         self.movieID = movieID
#         self.name = name
#         self.year = year
#         self.director = director

# # UserGroup Schema - for marshmallow
# class UserGroupSchema(ma.Schema):
#     class Meta: #all the variables you want to see
#         strict = True
#         fields = ('movieID','name','year','director')

# # Initiate Movie Schema
# usergroup_schema = UserGroupSchema()
# usergroups_schema = UserGroupSchema(many=True)

@application.route('/', methods=['GET'])
def default():
    return {'Does this work?':'YES!'}

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

@application.route('/rating/<userID>', methods = ['GET'])
def movie_option(userID):
    #this endpoint will take the user id and look through all the movies in the database that do not have a Yes/No choice made already by the user
    #it will then output one of those undecided options for the movie

    #code to unstub once schema created
    #movieInfo = ratings.filter_by(UserID = UserID, isLiked=NULL).first()
    #movieChoice = Movie.query.get(movieInfo.movieID)
    ##########output = {"response": str.(Movie.name)}
    #return jsonify (movieChoice)
    m = User.query.filter_by(userID=1).first()
    results = m.moviesRated
    ####movieInfo = m.users
    #stubbed output
    #movieChoice = {"movie": "TestMovie"}
    ###movieChoice = Movie.query.get(movieInfo.movieID)
    ###return jsonify (movieChoice)
    return jsonify({"Response": results})

# Run server
if __name__ == '__main__':
    #application.run(host='0.0.0.0') 
     application.run(debug=True)
