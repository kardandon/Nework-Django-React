const ERRORIMAGE = "https://merriam-webster.com/assets/mw/images/article/art-wap-landing-mp-lg/egg-3442-4c317615ec1fd800728672f2c168aca5@1x.jpg";
let q = 0;
const w = 10;
let ERROR = false;
document.addEventListener("DOMContentLoaded", () => {
    const id = getid();
    activate_profile(id);
});

function getid(){
    const a = window.location.pathname.split("/");
    return a[a.length-1];
}
function loaduser(id){
    fetch(`/api/profile/${id}`).then(res => {return res.json()}).then(data => {
        document.querySelector("#profilepic").src = data.profilepic;
        document.querySelector("#profilepic").onclick = () =>{profile(id)}
        document.querySelector("#username").innerHTML = data.username;
        document.querySelector("#followers").innerHTML = `follower: ${data.follower}`;
        document.querySelector("#followers").onclick = () => {activate_follow_list(id,"follower");};
        document.querySelector("#follows").innerHTML = `follows: ${data.follows}`;
        document.querySelector("#follows").onclick = () => {activate_follow_list(id,"followed");};
        document.querySelector("#changepic").innerHTML = "";
        if(data.change_profile_pic != undefined){
            document.querySelector("#changepic").innerHTML = "Change Profile Picture";
            document.querySelector("#changepic").onclick = () => {window.location.replace("/profilepic")}
        }
        document.querySelector("#followtext").innerHTML = "";
        if(data.user != undefined){
        document.querySelector("#followtext").innerHTML = data.follow_text;
        document.querySelector("#followtext").onclick = () => {follow(id);};
        }

    });
}

function loadfollowerlist(id,type)
{
    const list = document.querySelector("#follow_list");
    fetch(`/api/${type}/${id}?q=${q}&w=${w}`).then(
        res => {
            return res.json()}
    ).then( data => {
        if (data.list.length == 0) ERROR = true
        data.list.forEach(x => {
            adduser(x[0],x[1],x[2]);
        })
    }
    );
    q += w;
    return false;
}


function follow(id){
    const data = {"id": id};

    fetch(`/api/follow`, {
        method: "PUT", 
        body: JSON.stringify(data),
      }).then(res => {
        return res.json();
      }).then(data => {
        if(data.error){
        alert(data.error);}
        activate_profile(id)
      });
      return false;
}
function adduser(name,id,url){
    const list = document.querySelector("#follow_list");
    let user = document.createElement("div");
    user.classList.add("userlist-element")
    let username = document.createElement("h4");
    username.classList.add("username");
    username.innerHTML = name;
    user.onclick = () => {window.location.replace(`/profile/${id}`);};
    let profilepic = document.createElement("img");
    profilepic.classList.add("minipic");
    profilepic.src = url;
    profilepic.addEventListener("error", () => {profilepic.src = ERRORIMAGE});
    user.append(profilepic);
    user.append(username);
    list.append(user);
}
function activate_profile(id){
    loaduser(id)
    document.querySelector('#profile').style.display = 'block';
    document.querySelector('#follow_list').style.display = 'none';
}
function activate_follow_list(id,type){
    q = 0;
    const list = document.querySelector("#follow_list");
    list.innerHTML = "";
    let title = document.createElement("h1");
    title.innerHTML = `${type} list`;
    title.style.display = "flex";
    title.style.justifyContent = "center";
    list.append(title);
    ERROR = false
    loadfollowerlist(id,type)
    document.onscroll = () => {scrollcheck(id,type)};
    document.querySelector('#profile').style.display = 'none';
    document.querySelector('#follow_list').style.display = 'block';
    document.querySelector("#postlist").style.display = "none";
}

function scrollcheck(id,type){
    if(window.innerHeight + window.scrollY >= 0.9 * document.body.offsetHeight && !ERROR){
        loadfollowerlist(id,type)
    }
}