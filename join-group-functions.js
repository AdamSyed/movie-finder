const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

async function join_group(){
    //this function will take a user's ID and the inputted groupID and add that user to that group
    
    var group_ID = document.info.group_ID.value;    
	var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });
    console.log(vars.id); //gets the userID that has been passed
    
    const api_endpoint = 'join-group';
    
    const JOIN_GROUP_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/join-group';   

    //const response = await fetch(API_URL.concat(api_endpoint), {
    const response = await fetch(JOIN_GROUP_URL, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: vars.id,group_ID:group_ID})
    });

    const resp = await response.json();
    //resp = {'response':'User successfully added to group'};
    window.alert(resp['response']);
    console.log(resp);

    var redirect = 'http://findusamovie.s3-website-us-east-1.amazonaws.com/my-groups.html?id='+ vars.id;
    console.log(redirect);
    window.location.replace(redirect);
};

//NAVBAR STUFF
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
