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
    else if (pagina === '/loja/' || '/loja/<int:pk>/'){
        document.querySelector('#loja').querySelector('a').setAttribute('class', 'active')
    }
}
