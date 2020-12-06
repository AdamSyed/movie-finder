from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import numpy as np
from collections import Counter

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

    #def __init__(self,groupID,name,blacklist_threshold,max_size):
    def __init__(self,name,blacklist_threshold,max_size):
        #self.groupID = groupID
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
    print('before')
    email = request.json['email']
    password = request.json['password']
    print('request Done')
    user = User.query.filter_by(email=email, password=password).first()
    print('object checked')
    if bool(user) == True:
        output = {"response": str(user.userID)}
    else:
        output = {"response": "Invalid credentials."}
    print('output complete')
    return jsonify(output)

# ENDPOINT - Create user account
@application.route('/create',methods=['PUT'])
def create():
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    password = request.json['password']

    does_exists = User.query.filter_by(email = email).first()
    if(does_exists == None):    
        user = User(email,password,first_name,last_name)
        db.session.add(user)
        db.session.commit()

        user_id = User.query.filter_by(email = email).first().userID
        output = {'response':user_id}
    else:
        output = {'response':'email_duplicate'}
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
            output.append({'movieName':movie.name,'isLiked':m.isLiked,'movieID':movie.movieID})
    else:
        output = {"response": "Invalid ID."}

    return jsonify(output)

# ENDPOINT - Update a movie rating
@application.route('/update-rating',methods=['PUT'])
def update_rating():
    # print('request below ---------------')
    # print(request)
    ratings = request.json['ratings']
    output = {'response':'Success'}
    print(ratings)
    for r in ratings:
        userID = r['userID']
        movieID = r['movieID']
        isLiked = r['isLiked']
        try:
            rating = Userratesmovie.query.filter_by(userID=userID, movieID = movieID).first()
            rating.isLiked = isLiked

            db.session.commit()
        except:
            output['response'] = 'Error'
    return jsonify(output)

#ENDPOINT - display movies for a user to rate
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
        #clean this up so that we are displaying in JSON format instead of arrays bc that is more intuitive
        movieData = {'userID':userID, 'movieID':nextMovie.movieID, 'movie_name':nextMovie.name, 'movie_genre':nextMovie.genre, 'movie_director':nextMovie.director}
    except:
        movieData = {'userID':userID, 'movieID':'N/A', 'movie_name':'N/A', 'movie_genre':'N/A', 'movie_director':'N/A'}
    
    #finally, we return the results
    return jsonify(movieData)


 # ENDPOINT - User rating YES
@application.route('/rate-yes', methods = ['PUT'])
def rate_yes():
     userID = request.json['userID']
     movieID = request.json['movieID']
     
     newRecord = Userratesmovie(movieID,userID,True)

     db.session.add(newRecord)
     db.session.commit()
     # call method to display movie, will display a new unseen movie

     return ({'response':'Good'})
     # this method will insert into the user_rates_movie table 


# ENDPOINT - Get all movie rated by a user
@application.route('/my-groups',methods=['POST'])
def get_groups():
    id = request.json['id']
    
    user = User.query.filter_by(userID=id).first()

    if bool(user) == True:
        output = []
        for m in user.groups:
            group = Grp.query.filter_by(groupID = m.groupID).first()
            output.append({'groupName':group.name,'groupID':group.groupID})
    else:
        output = {"response": "Invalid ID."}

    return jsonify(output)


# ENDPOINT - User rating NO
@application.route('/rate-no', methods = ['PUT'])
def rate_no():
     userID = request.json['userID']
     movieID = request.json['movieID']
     
     newRecord = Userratesmovie(movieID,userID,False)

     db.session.add(newRecord)
     db.session.commit()
     # call method to display movie, will display a new unseen movie

     return ({'response':'Good'})
     # this method will insert into the user_rates_movie table 

# ENDPOINT - User rates movie
# This is an endpoint to consolidate the Yes and No separate endpoints, it will handle both
@application.route('/rated', methods = ['PUT'])
def rated():
     userID = request.json['userID']
     movieID = request.json['movieID']
     rated = request.json['rated']
     
     newRecord = Userratesmovie(movieID,userID,rated)

     db.session.add(newRecord)
     db.session.commit()
     # call method to display movie, will display a new unseen movie

     return ({'response':'Good'})
     # this method will insert into the user_rates_movie table 

#ENDPOINT - Create new group
@application.route('/create-group', methods = ['POST'])
def new_group():
    userID = request.json['id']
    groupName = request.json['group_name']
    #first create a group with that group name
    newGroup = Grp(groupName,None,None)
    db.session.add(newGroup)
    db.session.commit()

    #then, add the user to that group
    addToNewGroup = Useringroup(newGroup.groupID,userID, None, None)
    db.session.add(addToNewGroup)
    db.session.commit()
    
    return({'response':'Good'})

#ENDPOINT - Join new group
@application.route('/join-group', methods = ['POST'])
def join_group():
    userID = request.json['id']
    groupID = request.json['group_ID']
    
    test = Grp.query.filter_by(groupID=groupID).first()
    print(test)  
    if test is None:
        return({'response': 'Group does not exist'})

    #implement try-catch
    try:
        #Add user to specified group
        addToGroup = Useringroup(groupID,userID, None, None)
        db.session.add(addToGroup)
        db.session.commit()
    except:
        return({'response':'User already in group'})
        #return({'response':'Invalid Parameters'})
    
    return({'response':'User successfully added to group'})

# ENDPOINT - Group Home Page
@application.route('/group-info', methods = ['POST'])
def thisGroup():
    # userID = request.json['userID']
    groupID = request.json['groupID']
    #group = Grp.query.get(groupID)
    group = Grp.query.filter_by(groupID=groupID).first()
    
    # Group Name
                             
    # Group members

    #
    print(group)
    print(group.name)
    print(group.users)

    groupInfo = {'groupID':group.groupID, 'groupName':group.name}

    j = 1
    for i in group.users:
        print(i.userID)
        thisUser = User.query.filter_by(userID = i.userID).first()
        #print(thisUser.firstname)
        groupInfo['member'+str(j)] = thisUser.firstname
        j+=1

    groupInfo['size']=j-1

    return(jsonify(groupInfo))

@application.route('/group-results', methods = ['POST'])
def group_results():
    userID = request.json['id']
    groupID = request.json['groupID']

    ##logic
    #1.Get a list of all members in the group
    groupMembers = []
    groupMembers = Useringroup.query.filter_by(groupID = groupID).all()
    print(groupMembers)
    #2.Find the individual list of movies that each of those members have rated and 3.Filter so we have a list of all the movies that each member has rated a "yes" on
    memberMovie = []

    for j in groupMembers:
        ratings = Userratesmovie.query.filter_by(userID = j.userID).all()
        print(ratings)
        for k in ratings:
            if (k.isLiked == True):
                print(k.movieID)
                print(k.isLiked)
                memberMovie.append(k.movieID)
    print(memberMovie)

    #4.Get tallies for the number of ratings for each movie that members have rated "yes"
    tallies = Counter(memberMovie)
    print(tallies)
    #5.Sort the list in descending order of number of yes ratings
    top3 = tallies.most_common(3)
    print(top3)

    #remove the tally so we are left with the movie only 
    movieList = []
    for i in top3:
        movieList.append(i[0])

    #6.Filter out the movies that have been marked "watched" by the group
    #get the list of blacklisted movies for this group
    alreadyWatched = Usermovieblacklistvote.query.filter_by(groupID = groupID)
    watchedFilter = []
    for i in alreadyWatched:
        watchedFilter.append(i.movieID)
    print(watchedFilter)

    #use numpy to find the movies that aren't in 
    print(watchedFilter)
    print(movieList)
    topUnwatched = list(set(movieList).difference(watchedFilter))
    #print(unwatchedMovies)
    #7.Output the top 3 movies

    out = []
    for j in topUnwatched:
        out.append(Movie.query.filter_by(movieID = j).first().name)
        out.append(Movie.query.filter_by(movieID = j).first().movieID)
        out.append(Movie.query.filter_by(movieID = j).first().genre)
    
    while len(out) < 9:
        out.append('Please rate more movies to see more recommendations')
        out.append('N/A')
        out.append('N/A')

    print(out)
    recommendations = {'top_name': out[0], 'top_id': out[1], 'top_genre': out[2],'second_name': out[3], 'second_id': out[4], 'second_genre': out[5],'third_name': out[6],'third_id': out[7],'third_genre': out[8]}

    return (recommendations)

#ENDPOINT - Create new Watched Movie
@application.route('/group-watched', methods = ['PUT'])
def watched_Movie():
    groupID = request.json['groupID']
    movieID = request.json['movieID']
    userID = request.json['id']
    blacklist_vote = True

    watchedMovie=Usermovieblacklistvote(movieID,userID,groupID,blacklist_vote)

    db.session.add( watchedMovie)
    db.session.commit()
    
    return({'response':'Good'})

#ENDPOINT - Leave group
@application.route('/leave-group', methods = ['POST'])
def leave_group():
    userID = request.json['id']
    groupID = request.json['group_ID']

    #Remove user from group
    RemoveGroup = Useringroup.query.filter_by(groupID = groupID, userID = userID).delete()
    db.session.commit()
    
    return({'response':'You have successfully removed the group'})

# Run server
if __name__ == '__main__':
    application.run(host='0.0.0.0')
    #application.run(debug=True)
