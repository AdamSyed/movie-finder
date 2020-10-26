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
}

async function returnMovie() {
    //this function will return the movie
    //const api_endpoint = 'rating';

    //json.response == 'MovieName'
}