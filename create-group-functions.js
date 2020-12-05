const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

async function create_group(){
    //this function will create the new group in the database and add the creator to it
    
    var group_name = document.info.group_name.value;

    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });
    console.log(vars.id); //gets the userID that has been passed
    
    const api_endpoint = 'create-group';
    
    const CREATE_GROUP_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/create-group';   

    //const response = await fetch(API_URL.concat(api_endpoint), {
    const response = await fetch(CREATE_GROUP_URL, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: vars.id,group_name:group_name})
    });

    const resp = await response.json();
    console.log(resp);

    //REPLACE THIS REDIRECT SECTION WITH THE HTML OF THE MY GROUPS PAGES
    var redirect = 'http://findusamovie.s3-website-us-east-1.amazonaws.com/my-groups.html?id='+ vars.id;
    console.log(redirect);
    window.location.replace(redirect);
};

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
