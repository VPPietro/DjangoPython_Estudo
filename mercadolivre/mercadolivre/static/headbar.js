var page = document.getElementById('title').innerText

var usuario = document.getElementById('usuario').innerText
document.getElementById('usuario').innerHTML = ""



if (usuario == 'AnonymousUser'){
    document.getElementById('list').innerHTML = 
        '<li><a href="/user/login/">Login</a></li>'
}
else{
    document.getElementById('list').innerHTML=
        '<li><a href="/index/" id="UserLogado">Logado como: {{ usuario }}</a></li>' +
        '<li><a href="/user/logoff">Logoff</a></li>'
        console.log(page + " " + usuario)
}