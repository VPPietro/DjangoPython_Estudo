const nome = document.querySelector('#id_nome');
const email = document.querySelector('#id_email');
const senha = document.querySelector('#id_senha')


nome.insertAdjacentHTML('beforebegin', '<strong>Nome: </strong>')
email.insertAdjacentHTML('beforebegin', '<strong>E-mail: </strong>')
senha.insertAdjacentHTML('beforebegin', '<strong>Confirme a senha: </strong>')

