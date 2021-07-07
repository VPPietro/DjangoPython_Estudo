const nomeButton = document.querySelector('#nomeBtn')
const nomeLi = document.querySelector('#nome')

nomeButton.addEventListener('click', abreFormularioNome)

function abreFormularioNome(){
    if (nomeButton.value === 'Alterar'){
        document.getElementById('teste').innerHTML = 
        document.getElementById('teste2').innerHTML +
        '<input type="submit">'
    }
    else if (nomeButton.value === 'Cancelar'){
        
    }
}