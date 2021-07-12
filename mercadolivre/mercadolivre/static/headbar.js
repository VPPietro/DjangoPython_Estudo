var page = document.getElementById('title').innerText

var usuario = document.getElementById('usuario').innerText
document.getElementById('usuario').innerHTML = ""

var superuser = document.getElementById('superuser').innerText
document.getElementById('superuser').innerHTML = ""


function activate_page(pagina){
    if (pagina === '/index/' || pagina === '/'){
        document.querySelector('#index').querySelector('a').setAttribute('class', 'active')
    }
    else if (pagina === '/user/signup/'){
        document.querySelector('#signup').querySelector('a').setAttribute('class', 'active')
    }
    else if (pagina === '/user/login/'){
        document.querySelector('#login').querySelector('a').setAttribute('class', 'active')
    }
    else if (pagina === '/user/info/' || pagina === '/user/alterinfo/'){
        document.querySelector('#userinfo').querySelector('a').setAttribute('class', 'active')
    }
}


if (usuario == 'AnonymousUser'){
    document.getElementById('list').innerHTML =
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li class="LoginOut" id="login"><a href="/user/login/">Login</a></li>'+
        '<li class="LoginOut" id="signup"><a href="/user/signup/">Sign Up</a></li>'
    activate_page(location.pathname)
}
else{
    document.getElementById('list').innerHTML=
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li id="logoff" class="LoginOut"><a href="/user/logoff">Logout</a></li>' +
        '<li id="userinfo" class="LoginOut"><a href="/user/info">Logado como: '+ usuario +'</a></li>';
        if (superuser === 'True'){
            document.getElementById('list').innerHTML +='<li id="adminpg"><a href="/admin">ADMIN</a></li>'
        }
    activate_page(location.pathname)
}
console.log(superuser)