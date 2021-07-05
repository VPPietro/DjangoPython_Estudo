var page = document.getElementById('title').innerText

var usuario = document.getElementById('usuario').innerText
document.getElementById('usuario').innerHTML = ""

function activate_page(pagina){
    if (pagina === 'Home'){
        document.getElementById('index').innerHTML = 
        '<a href="/index/" class="active">Home</a>'
    }
    else if (pagina === 'Login'){
        document.getElementById('login').innerHTML =
        '<a href="/user/login/" class="active">Login</a>'
    }
    else if (pagina === 'Signin'){
        document.getElementById('signin').innerHTML = 
        '<a href="/user/signin/" class="active">Sign In</a>'
    }
    else if (pagina === 'User Info'){
        document.getElementById('userinfo').innerHTML = 
        '<a href="/user/info" class="active">Logado como: '+ usuario +'</a>'
    }
}

if (usuario == 'AnonymousUser'){
    document.getElementById('list').innerHTML = 
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li class="LoginOut" id="login"><a href="/user/login/">Login</a></li>'+
        '<li class="LoginOut" id="signin"><a href="/user/signin/">Sign In</a></li>' +
        '<li id="userinfo"><a href="/user/info">User info temp</a></li>'
    activate_page(document.getElementById('title').innerText)
}
else{
    document.getElementById('list').innerHTML=
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li id="logoff" class="LoginOut"><a href="/user/logoff">Logout</a></li>' +
        '<li id="userinfo" class="LoginOut"><a href="/user/info">Logado como: '+ usuario +'</a></li>'
    activate_page(document.getElementById('title').innerText)
}
