const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

window.onload = async function(){
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });

    const api_endpoint = 'all-movie-ratings';

    const response = await fetch(API_URL.concat(api_endpoint), {
         method: 'POST',
         headers: {
             'Content-Type':'application/json'
         },
         body: JSON.stringify({id:vars.id})
    });

    const json = await response.json();

    //this line below is used for testing
    //json = [{"isLiked": true,"movieName": "The Proposal"},{"isLiked": false,"movieName": "Inception"}];
    var output_html = "";
    console.log(json.length);
    console.log(json);

    for (var i = 0; i<json.length; i++){
        var movieName = json[i]['movieName'];
        var isLiked = json[i]['isLiked'];
        
        if (isLiked == false){
            output_html = output_html +  "<h3>"+movieName+"</h3> <label for=\"like\" class=\"label\">Liked</label><input type=\"radio\" id=\"like\" name=\""+movieName+"\" value= \"true\" ><br><label for=\"dislike\" class=\"label\">Disliked</label><input type=\"radio\" id=\"dislike\" name=\""+movieName+"\" value= \"false\" checked ><br>  "
        }
        if (isLiked == true){

           output_html = output_html + "<h3>"+movieName+"</h3> <label for=\"like\" class=\"label\">Liked</label><input type=\"radio\" id=\"like\" name=\""+movieName+"\" value= \"true\" checked ><br><label for=\"dislike\" class=\"label\">Disliked</label><input type=\"radio\" id=\"dislike\" name=\""+movieName+"\" value= \"false\"  ><br>  "
        }
    }
    console.log(output_html);
    document.getElementById('dynamic_results').innerHTML = output_html;
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


    if (first_name == '' | last_name == '' | email == '' | password == ''){
        document.getElementById('saved').innerHTML = 'Please fill in all of the fields.';
    } else{
        const response = await fetch(API_URL.concat(api_endpoint,vars.id), {
            method: 'PUT',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({firstname:firstname,lastname:lastname,email:email,password:password,id:vars.id})
        });
        const json = await response.json();
        console.log(json.response);
        
        if (json.response == 'Success'){
            document.getElementById('saved').innerHTML = "We've updated your profile!";
        } else {
            document.getElementById('saved').innerHTML = "We were unable to succesfully update your profile, please contact our support team.";
        }
    }    
}

function redirect(page) {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/'+ page + '.html?id=' + vars.id);
}