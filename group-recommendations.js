const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

//Array that will house the inserted movieIDs
var movies = [7, 8,9]

async function groupMovies() {
    //this function will return the movie

    // const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/rating/1';
    const RETURN_MOVIE_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/group-results';
    
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
        body: JSON.stringify({id: vars.id,groupID: vars.groupId})
    });

    const jsonFile = await response.json();


	console.log(jsonFile);

    //'top_name': out[0], 'top_id': out[1], 'top_genre': out[2],'second_name': out[3], 'second_id': out[4], 'second_genre': out[5],'third_name': out[6],'third_id': out[7],'third_genre': out[8],}


    //load the movieID array with the new movieID's
    movies[0] = jsonFile["top_id"];
    movies[2] = jsonFile["second_id"];
    movies[3] = jsonFile["third_id"];


    //assign the Javascript values to the approporate HTML sections for diplay
    document.getElementById('first').innerHTML = jsonFile["top_name"];
    document.getElementById('first_genre').innerHTML = jsonFile["top_genre"];
    document.getElementById('second').innerHTML = jsonFile["second_name"];
    document.getElementById('second_genre').innerHTML = jsonFile["second_genre"];
    document.getElementById('third').innerHTML = jsonFile["third_name"];
    document.getElementById('third_genre').innerHTML = jsonFile["third_genre"];

}

function redirectRating() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/rating.html?id=' + vars.id);
}
function redirectProfile() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/user-profile.html?id=' + vars.id);
}
function redirectGroup() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/my-groups.html?id=' + vars.id);
}

// Send info to the next page
async function setWatched(movieID) {
    // window.alert(movieID);
    //window.location.change("www.moviefinder.com/group-home.html);
    
}

//Function that sends the watched movieID userID and groupID to the endpoint and refreshes the page
async function setWatched(movieIndex) {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    currentID = vars.id;
    const api_endpoint = 'group-watched';

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: vars.id, movieID: movies[movieIndex], groupID: vars.groupId })
    });
    //Alert for testing
    //window.alert(movies[movieIndex]);
    const json = await response.json();
    window.location.replace("http://findusamovie.s3-website-us-east-1.amazonaws.com/group-results.html?id=" + vars.id + "&groupId=" + vars.groupId);
}