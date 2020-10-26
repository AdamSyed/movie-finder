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


//function to pass info to backend when user clicks they like the displayed movie
async function clickedYes() {
    const api_endpoint = 'rate-yes';
    // currently assumed these parameters are available
//movieID
//userID
    //will need to change following based on rafiq's code
    var movieID = document.credentials.Email.value;
    var userID = document.credentials.Email.value;

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userID: userID, movieID: movieID})
    });

    const json = await response.json();

    //call rafiq function for next movie
/*    if (json.response == 'Invalid credentials.') {
        document.getElementById('invalid').innerHTML = 'Invalid credentials';
    } else {
        window.location.replace('http://www.schoolfit.me.s3-website-us-east-1.amazonaws.com/results.html?id=' + json.response);
    }*/


function create(){
        window.location.replace('https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/create_user.html')
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
    var redirect = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/create_user.html?luserid=' + json.response;
    console.log(redirect)
    window.location.replace(redirect);

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

