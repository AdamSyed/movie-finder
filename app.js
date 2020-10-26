const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

async function login(){
    const api_endpoint = 'login';
    var email = document.credentials.Email.value;
    var password = document.credentials.Password.value;
    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({email:email,password:password})
    });
    const json = await response.json();
    if (json.response == 'Invalid credentials.'){
         document.getElementById('invalid').innerHTML = 'Invalid credentials';
    } else {
        window.location.replace('http://www.schoolfit.me.s3-website-us-east-1.amazonaws.com/results.html?id='+json.response);
    }
}

async function returnMovie() {
    //this function will return the movie
    const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/rating/';   

    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });

    const response = await fetch(RETURN_MOVIE_URL.concat(vars), {
    //const response = await fetch(RETURN_MOVIE_URL.concat(), {
    //const response = await fetch(RETURN_MOVIE_URL, {
        method: 'GET'
    });
    const jsonFile = await response.json();

	console.log(jsonFile);
    
    var movieName = jsonFile[3];
    var genre = jsonFIle [4];
    //document.write(movie);
    document.write(movieName);
    document.write("<br>");
    document.write(genre);
   //json.response == 'MovieName'
}