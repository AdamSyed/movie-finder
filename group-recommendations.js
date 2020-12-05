const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

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
        body: JSON.stringify({id: vars.id,groupID: vars.groupID})
    });

    const jsonFile = await response.json();

    jsonFile = {
        "top_name": "My Marks",
        "top_genre": "Tragedy",
        "second_name": "Murder on the Orient Express",
        "second_genre": "Mystery",
        "third_name": "Inception",
        "third_genre": "Action",
    };

	console.log(jsonFile);

    //'top_name': out[0], 'top_id': out[1], 'top_genre': out[2],'second_name': out[3], 'second_id': out[4], 'second_genre': out[5],'third_name': out[6],'third_id': out[7],'third_genre': out[8],}
        

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
