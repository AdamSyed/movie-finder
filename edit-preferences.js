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

    // this line below is used for testing
    //json = [{"isLiked": true,"movieName": "The Proposal","movieID": 1},{"isLiked": false,"movieName": "Inception","movieID": 2}];
    var output_html = "";
    
    for (var i = 0; i<json.length; i++){
        var movieName = json[i]['movieName'];
        var isLiked = json[i]['isLiked'];
        var movieID = json[i]['movieID']

        if (isLiked == false){
            output_html = output_html +  "<h3>"+movieName+"</h3> <label for=\"like\" class=\"label\">Liked</label><input type=\"radio\" id=\"like\" name=\""+movieID+"\" value= \"true\" ><br><label for=\"dislike\" class=\"label\">Disliked</label><input type=\"radio\" id=\"dislike\" name=\""+movieID+"\" value= \"false\" checked ><br>  "
        }
        if (isLiked == true){

           output_html = output_html + "<h3>"+movieName+"</h3> <label for=\"like\" class=\"label\">Liked</label><input type=\"radio\" id=\"like\" name=\""+movieID+"\" value= \"true\" checked ><br><label for=\"dislike\" class=\"label\">Disliked</label><input type=\"radio\" id=\"dislike\" name=\""+movieID+"\" value= \"false\"  ><br>  "
        }
    }
    document.getElementById('dynamic_results').innerHTML = output_html;
};

async function update_preferences(){
    const api_endpoint = 'update-rating';
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    var form = document.getElementById("myform");
    var radios = form.querySelectorAll('input[type=radio]');
    var i;
    var lst = [];
    for (var i = 0; i < form.length; i++) {
        var child = form.getElementsByTagName('input')[i];
        if(child.checked == true){
            if(child.id== 'like'){
                lst.push({
                    "isLiked" : true,
                    "movieID" : parseInt(child.name),
                    "userID"  : vars.id  
                })
            }
        }
        if(child.checked == true){
            if(child.id== 'dislike'){
                lst.push({
                    "isLiked" : false, 
                    "movieID" : parseInt(child.name),
                    "userID"  : vars.id
                })
            }
        }
    }
    const response = await fetch(API_URL.concat(api_endpoint), {
        method: 'PUT',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({ratings : lst})
    });
    const json = await response.json();

    if (json.response == 'Success'){
        document.getElementById('saved').innerHTML = "We've updated your movie ratings!";
    } else {
        document.getElementById('saved').innerHTML = "We were unable to succesfully update your movie ratings, please contact our support team.";
    }
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

