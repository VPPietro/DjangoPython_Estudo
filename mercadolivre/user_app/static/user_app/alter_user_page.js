const nomeButton = document.querySelector('#nome').querySelector('input')

nomeButton.addEventListener('click', abreFormularioNome)

function abreFormularioNome(){
    console.log(nomeButton.querySelector('input'))
    // if (nomeButton.querySelector('button') === ''){
    document.getElementById('nome').innerHTML = 
    '<strong>Nome completo:</strong>' +
    '<input type="text"></input>' +
    '<input type="button" value="Salvar"></input>'
    
}