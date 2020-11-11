const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

function redirectPost(url, id) {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = url;

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = "id";
    input.value = id;
    form.appendChild(input);

    form.submit();
}

async function login(){
    const api_endpoint = 'login';
    var email = document.credentials.Email.value;
    var password = document.credentials.Password.value;
    console.log(email);
    console.log(password);
    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({email:email,password:password})
    });
    console.log('json')
    const json = await response.json();
    console.log(json)
    if (json.response == 'Invalid credentials.'){
        document.getElementById('invalid').innerHTML = 'Invalid credentials';
    } else {
        var redirect = 'http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=' + json.response;
        window.location.replace(redirect);
    }
}

function create(){
    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/create-user.html')
}

async function create_user(){
    const api_endpoint = 'create';
    var first_name = document.info.first_name.value;
    var last_name = document.info.last_name.value;
    var email = document.info.email.value;
    var password = document.info.password.value;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({first_name:first_name,last_name:last_name,email:email,password:password})
    });
    const json = await response.json();
    console.log(json.response);
    var redirect = 'http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id='+json.response;
    console.log(redirect);
    window.location.replace(redirect);
}

// declaring global varibles to be used across functions
var activeMovieID = 1;
var activeMovieName = "Knives Out";

async function returnMovie() {
    //this function will return the movie

    // const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/rating/1';
    const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/rating';
    //console.log("reached here");
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });
    console.log(vars.id); //gets the userID that has been passed

    //const response = await fetch(RETURN_MOVIE_URL.concat(vars), {
    const response = await fetch(RETURN_MOVIE_URL, {
    
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: vars.id})
    });

    const jsonFile = await response.json();

    //leaving a hardcoded test here that we can swap out for unit tests as needed
    //jsonFile = {
    //    "movieID": 9,
    //    "movie_director": "Rian Johnson",
    //    "movie_genre": "Comedy",
    //    "movie_name": "Knives Out",
    //    "userID": 1
    //};
	console.log(jsonFile);
    

    //from the jsonFile: 0 = id, 1 = movieID, 2 = movie name, 3 = genre,4 = director; will add 5 = image, 6 to end = actors in later sprints as needed 


    //assign the Javascript values to the approporate HTML sections for diplay
    document.getElementById('movie_name').innerHTML = jsonFile["movie_name"];
    document.getElementById('movie_genre').innerHTML = jsonFile["movie_genre"];
    document.getElementById('movie_director').innerHTML = jsonFile["movie_director"];

    //update the global activeMovieID variable to the current movie so that it can be properly allocated when the yes/no buttons are clicked.
    activeMovieID = jsonFile["movieID"];
    activeMovieName = jsonFile["movie_name"];
   //json.response == 'MovieName'
}

//function to pass info to backend when user clicks they like the displayed movie
async function clickedYes() {
    //Grab the active userID from URL
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });
    //log IDs
    console.log(vars.id);
    console.log(activeMovieID);

    const api_endpoint = 'rate-yes';
    
    //set variables to IDs
    var movieID = activeMovieID;
    var userID = vars.id;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({userID:userID,movieID:movieID})
    });
    const resp = await response.json();
    console.log(resp);
    //window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=' + json.response);
    window.location.reload();
}

//function to pass info to backend when user clicks they dislike the displayed movie
async function clickedNo() {
    //Grab the active userID from URL
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    //log IDs
    console.log(vars.id);
    console.log(activeMovieID);

    const api_endpoint = 'rate-no';

    //set variables to IDs
    var movieID = activeMovieID;
    var userID = vars.id;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userID:userID, movieID:movieID })
    });
    const resp = await response.json();
    console.log(resp);
    //window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=' + json.response);
    window.location.reload();
}

async function clickedRating(rating) {
    //Grab the active userID from URL
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    //log IDs
    console.log(vars.id);
    console.log(activeMovieID);
    console.log(rating);

    const api_endpoint = 'rated';

    //set variables to IDs
    var movieID = activeMovieID;
    var userID = vars.id;
    var rated = rating;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userID: userID, movieID: movieID,rated: rated })
    });
    const resp = await response.json();
    console.log(resp);
    //window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=' + json.response);
    window.location.reload();
}


async function viewIMDB() {
    var movieSearch = activeMovieName.replace(" ", "+");
    var imdb = "https://www.imdb.com/find?q=" + movieSearch;
    console.log(imdb);
    window.open(imdb);
}
async function viewTrailer() {
    var movieSearch = activeMovieName.replace(" ", "+");
    var yt = "https://www.youtube.com/results?search_query=" + movieSearch + "+trailer";
    console.log(yt);
    window.open(yt);
}