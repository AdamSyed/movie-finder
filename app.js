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
        redirectPost('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html', json.response);
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

var activeMovieID = 1;

async function returnMovie() {
    //this function will return the movie

    // const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/rating/1';
    const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/rating';
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });
    console.log(vars.id);

    const response = await fetch(RETURN_MOVIE_URL.concat(vars), {
    //const response = await fetch(RETURN_MOVIE_URL.concat(), {
    //const response = await fetch(RETURN_MOVIE_URL, {
        method: 'POST' 
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
    activeMovieID= jsonFile["movieID"];
   //json.response == 'MovieName'
}

//function to pass info to backend when user clicks they like the displayed movie
async function clickedYes() {

    //added a console output to validate that the global activeMovieID variable is working as intended.
    //@jaad, use the variable activeMovieID to get the movie ID that is currently being rated
    console.log(activeMovieID);
    const api_endpoint = 'rate-yes';
    // currently assumed these parameters are available
    //movieID
    //userID
    //will need to change following based on rafiq's code

    var movieID = 9;
    var userID = 1;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userID: userID, movieID: movieID})
    });

    const json = await response.json();
    console.log(json.response);

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=' + json.response);
    //window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=1');
}
async function clickedNo() {

    const api_endpoint = 'rate-no';
    // currently assumed these parameters are available
    //movieID
    //userID
    //will need to change following based on rafiq's code

    var movieID = 8;
    var userID = 1;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userID: userID, movieID: movieID})
    });

    const json = await response.json();
    
    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id='+json.response);

}