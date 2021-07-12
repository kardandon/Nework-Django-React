const ERRORIMAGE = "https://merriam-webster.com/assets/mw/images/article/art-wap-landing-mp-lg/egg-3442-4c317615ec1fd800728672f2c168aca5@1x.jpg";
function Post(props){
    const x = () => {window.location.replace(`/profile/${props.post.id}`)};
    const y = () => {
        fetch("/like",{
            method: "PUT",
            body: JSON.stringify({"id": props.post.postid}),
        }).then(x => {return x.json()}).then(data => {props.update();})
        return false
    }
    const editpost = (e) => {
        if ( (window.event ? event.keyCode : e.which) == 13){
            fetch("/editpost",{
                method: "PUT",
                body:JSON.stringify({"text": e.target.value, "id": props.post.postid})
            }).then(x => {return x.json()}).then(data => {window.location.reload();});
            return false;
        }
    }
    const z = (e) => {
        if (props.post.is_user){
            const temp = <textarea class='text' style={{resize: "none"}} onKeyDown={editpost}>{props.post.text}</textarea>
            ReactDOM.render(temp, e.target.parentNode)
        }
        return false
    }
    return(
        <div class="post">
            <div onClick={x} class="userinfo">
            <img class="minipic" src={props.post.profilepic} onError={(e)=>{e.target.onerror = null; e.target.src=ERRORIMAGE;}}></img>
            <p class="username">{props.post.username}</p>
            </div>
            <div class="post-inner">
            <div class="post-header">
                <p class="timestamp">{props.post.timestamp}</p>
                <p class="like" onClick={y}> Like: {props.post.likes}</p>
            </div>
            <div style={{width: "100%"}}>
                <p class="text" onClick={z}>{props.post.text}</p>
                </div>
            </div>
        </div>
    )
}

function submitpost(){
    const text = document.querySelector("#newpost").value;
    fetch("/send",{
        method: "PUT",
        body:JSON.stringify({"text": text})
    }).then(res => {//window.location.reload();
    });
    return false;
    
}
function PostList(props){
    let items = [];
    props.posts.forEach(post => {
        items.push(<Post post={post} update={props.update}/>);
    });
    return (
        <div class="postlist">
            {items}
        </div>
    )
}


function NewPost(props){
    return(
        <div class="postlist">
            <form class="post" onSubmit={submitpost}>
                <input class="newpost-input" type="text" name="post" id="newpost"/>
                <input class="newpost-submit" type="submit"/>
            </form>
        </div>
    );
}

function PageButton(props){
    return(<button class="post-buttons" onClick={props.onClick} >{props.name}</button>)
}

class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            page: "allposts",
            initial: 0,
            length: 10,
            page_continue: true,
            posts: [],
        };
        this.back = this.back.bind(this);
        this.next = this.next.bind(this);
        this.update = this.update.bind(this);
        document.querySelector("#allposts").onclick = () => {
            this.setState({
                ...this.state,
                "page": "allposts",
            })
            this.update();
            return false
        }
        if (document.querySelector("#login") == null){
        document.querySelector("#follow").onclick = () => {
            this.setState({
                ...this.state,
                "page": "follower",
            })
            this.update();
            return false;
        }}
    }
    
    componentDidMount() {
        fetch(`/posts?q=${this.state.initial}&w=${this.state.length}&e=0&f=${this.state.page}`)
        .then(res => {return res.json()})
        .then(data => {
            let cont = true;
            if (this.state.length != data.data.length){
                cont = false;
            }
            this.setState({
                ...this.state,
                "page_continue": cont,
                "posts": data.data,
            })
        });
    }
    update(){
        fetch(`/posts?q=${this.state.initial}&w=${this.state.length}&e=0&f=${this.state.page}`)
        .then(res => {return res.json()})
        .then(data => {
            let cont = true;
            if (this.state.length != data.data.length){
                cont = false;
            }
            this.setState({
                ...this.state,
                "page_continue": cont,
                "posts": data.data,
            })
            this.render()
        });
    }

    back(){
        let asd = this.state;
        asd.initial = asd.initial - asd.length;
        this.setState(asd);
        this.update();
    }
    next(){
        let asd = this.state;
        asd.initial = asd.initial + asd.length;
        this.setState(asd);
        this.update();
    }
    render(){
        
        let out = [];
        if(this.state.page == "allposts"){
            out.push(<NewPost/>);
        }
        else{
            out.push(<div class="postlist"><h1 class="post">Following</h1></div>)
        }
        out.push(<PostList posts={this.state.posts} update={this.update}/>);
        if(this.state.length <= this.state.initial){
            out.push(<PageButton name="back" onClick={this.back}/>);
        }
        if(this.state.page_continue)
        {
            out.push(<PageButton name="next" onClick={this.next}/>);
        }
        //this.setState(asd);
        return(out);
    }
}
ReactDOM.render(<App/>, document.querySelector("#app"));