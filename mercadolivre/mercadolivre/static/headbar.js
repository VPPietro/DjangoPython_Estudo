var page = document.getElementById('title').innerText

var usuario = document.getElementById('usuario').innerText
document.getElementById('usuario').innerHTML = ""


function activate_page(pagina){
    console.log(pagina)
    if (pagina === '/index/' || pagina === '/'){
        document.querySelector('#index').querySelector('a').setAttribute('class', 'active')
    }
    else if (pagina === '/user/signin/'){
        document.querySelector('#signin').querySelector('a').setAttribute('class', 'active')
    }
    else if (pagina === '/user/login/'){
        document.querySelector('#login').querySelector('a').setAttribute('class', 'active')
    }
    else if (pagina === '/user/info/'){
        document.querySelector('#userinfo').querySelector('a').setAttribute('class', 'active')
    }
}


if (usuario == 'AnonymousUser'){
    document.getElementById('list').innerHTML = 
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li class="LoginOut" id="login"><a href="/user/login/">Login</a></li>'+
        '<li class="LoginOut" id="signin"><a href="/user/signin/">Sign In</a></li>'
    activate_page(location.pathname)
}
else{
    document.getElementById('list').innerHTML=
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li id="logoff" class="LoginOut"><a href="/user/logoff">Logout</a></li>' +
        '<li id="userinfo" class="LoginOut"><a href="/user/info">Logado como: '+ usuario +'</a></li>'
    activate_page(location.pathname)
}
