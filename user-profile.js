const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

window.onload = async function(){
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    const api_endpoint = 'user-preferences';

    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({id:vars.id})
    });

    const json = await response.json();

    document.getElementById('first_name').value = json.firstname;
    document.getElementById('last_name').value = json.lastname;
    document.getElementById('email').value = json.email;
    document.getElementById('password').value = json.password;
};

async function update(){
    const api_endpoint = 'update-user-preferences';
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });

    var firstname = document.info.first_name.value;
    var lastname = document.info.last_name.value;
    var email = document.info.email.value;
    var password = document.info.password.value;

    const response = await fetch(API_URL.concat(api_endpoint,vars.id), {
        method: 'PUT',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({firstname:firstname,lastname:lastname,email:email,password:password})
    });
    const json = await response.json();
    console.log(json.response);
    
    if (json.response == 'Success'){
        document.getElementById('saved').innerHTML = "We've updated your profile!";
    } else {
        document.getElementById('saved').innerHTML = "We were unable to succesfully update your profile, please contact our support team.";
    }
}

function redirect(page) {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/'+ page + '.html?id=' + vars.id);
}