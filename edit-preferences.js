const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

window.onload = async function(){
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    const api_endpoint = 'all-movie-ratings';


    // const response = await fetch(API_URL.concat(api_endpoint), {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type':'application/json'
    //     },
    //     body: JSON.stringify({id:vars.id})
    // });

    // const json = await response.json();

    json = [{"isLiked": false,"movieName": "The Proposal"},{"isLiked": false,"movieName": "Inception"}];
    var ouptut_html = "";
    console.log(json.length);
    console.log(json);

    // <input type="radio" id="male" name="gender" value="male">
    // <label for="male">Male</label><br>
    // <input type="radio" id="female" name="gender" value="female">
    // <label for="female">Female</label><br>
  

    for (var i = 0; i<json.length; i++){
        var movieName = json[i]['movieName'];
        var isLiked = json[i]['isLiked'];
        ouptut_html = ouptut_html + "<label for=\"" + movieName + "\" class=\"label\">" + movieName + "</label><input type=\"radio\" id=\""+ movieName + "\" name=\""+ movieName +"\"<br>"
    }
    console.log(ouptut_html);
    document.getElementById('dynamic_results').innerHTML = ouptut_html;
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