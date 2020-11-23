const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';


function redirect(page) {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });

    window.location.replace('http://findusamovie.s3-website-us-east-1.amazonaws.com/'+ page + '.html?id=' + vars.id);
}

async function LoadGroups(){
     var vars = {};
     var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
     });
  currentID=vars.id;
     const api_endpoint = 'my-groups';
 
     const response = await fetch(API_URL.concat(api_endpoint), {
         method: 'POST',
         headers: {
            'Content-Type':'application/json'
         },
      body: JSON.stringify({id:vars.id})
     });
 
    const json = await response.json();
 
     //this line below is used for testing
   // json = [{"groupID": 63,"groupName": "The boys"},{"groupID": 36,"groupName": "The gurls"}];
    
   // Line to test if actually outputing
  // var output_html = " HI";
     var output_html = " <table cellspacing=0 cellpadding=0>";
     console.log(json.length);
     console.log(json);
 
     for (var i = 0; i<json.length; i++){
            var groupID = json[i]['groupID'];
            var groupName = json[i]['groupName'];
            
        
           output_html =   output_html +   "<tr><td style=\"text-align: right\"><b style=\"font-size: 30px\">Group ID:</b> </td> <!--Pass Group ID into here--><td> <p id=\"group_id\" style=\"font-size:30px\"> "+ groupID + "</p></td> <td style=\"text-align: right\"><b style=\"font-size: 30px\">Group Name:</b> </td><!--Pass Group Name into here--><td><p id=\"group_name\" style=\"font-size:30px\"> "+ groupName + "</p></td><td> <button style=\"font-size:30px\" type=\"button\" onclick=\"OpenGroup("+ groupID + ")\">Open Group</button></td></tr>"  

    // basic version to test if working
   // output_html =   output_html +" <tr> <td> <p > "+ groupID + "</p> </td> <td> <p > "+ groupName + " </p> </td>  <td> <input class=\"button is-info\" style=\"width:100%;\" type=\"button\" value=\"Update\" onClick=\"update_preferences()\">  </td> </tr>"
                                  
   
        };
     
 
       
    output_html =   output_html + "</table>"
    console.log(output_html);
    document.getElementById('dynamic_results').innerHTML = output_html;    

   
    //async function groupRedirect(int id){
    // window.location.change("www.moviefinder.com/group?groupId="+ id);
}

 // Send info to the next page
async function OpenGroup(id){
   // window.alert(id);
    //window.location.change("www.moviefinder.com/group-home.html);
   window.location.replace("http://findusamovie.s3-website-us-east-1.amazonaws.com/group-home.html?groupId="+ id)
}

async function createGroup(){

     var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
       vars[key] = value;
    });

   //window.alert(vars.id);
 
   window.location.replace("http://findusamovie.s3-website-us-east-1.amazonaws.com/create-group.html?id="+ vars.id)
}