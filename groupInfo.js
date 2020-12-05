// JavaScript source code
//const API_URL = 'https://cors-anywhere.herokuapp.com/http://moviefinder.us-east-1.elasticbeanstalk.com/';

async function Info() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    console.log(vars.groupID); //gets the groupID that has been passed

    const response = await fetch(API_URL.concat("group_info"), {
    //const response = await fetch(RETURN_MOVIE_URL, {

        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ groupID: vars.groupID })
    });

    const jsonFile = await response.json();
    //const jsonFile = { "groupID": 1, "groupName": "Test Group", "member1": 1, "member2": 3, "member3": 4, "size": 3 }

    var i = 1;
    var members = '';
    var currMem = "";
    for (i = 1; i <= jsonFile["size"]; i++) {
        currMem = 'member'+i.toString();
        console.log(currMem);
        members += jsonFile[currMem].toString();
        if (i < jsonFile["size"]) {
            members += ', ';
        }
    }
    console.log(members);
    document.getElementById('group_name').innerHTML = jsonFile["groupName"];
    document.getElementById('group_ID').innerHTML = jsonFile["groupID"];
    document.getElementById('group_members').innerHTML = members;
}