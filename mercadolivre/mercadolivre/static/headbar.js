var page = document.getElementById('title').innerText

var usuario = document.getElementById('usuario').innerText
document.getElementById('usuario').innerHTML = ""



if (usuario == 'AnonymousUser'){
    document.getElementById('list').innerHTML = 
        '<li id="index"><a href="/index/">Home</a></li>'+
        '<li id="login"><a href="/user/login/">Login</a></li>'+
        '<li id="signin"><a href="/user/signin/">Sign In</a></li>'
    console.log(usuario)
    pagina = document.getElementById('title').innerText
    if (pagina === 'Home'){
        document.getElementById('index').innerHTML = 
        '<a href="/index/" id="index" class="active">Home</a>'
    }
    else if (pagina === 'Login'){
        document.getElementById('login').innerHTML =
        '<a href="/user/login/" class="active">Login</a>'
    }
    else if (pagina === 'Signin'){
        document.getElementById('signin').innerHTML = 
        '<a href="/user/signin/" class="active">Sign In</a>'
    }
    else{
        console.log(pagina)
    }
}
else{
    document.getElementById('list').innerHTML=
        '<li><a href="/index/" id="index">Home</a></li>'+
        '<li><a href="/user/logoff">Logout</a></li>' +
        '<li><a href="/index/" id="UserLogado">Logado como: '+ usuario +'</a></li>'
        console.log(page + " " + usuario)
}
