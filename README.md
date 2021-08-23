# Django_Eshop_Estudo
Estudo de desenvolvimento de site com Django/Python e CSS, JavaScript, MySQL.

Status atual (08/08/2021)
Criado dois aplicativos: user_app e loja_app

user_app gerencia: 
  * Login do user
  * Cadastro do user
  * Logoff do user
  * Página de info do user
  * Página de atualização de info do user

loja_app gerencia:
  * Listagem de itens (página index)
  * Listagem de itens do user
  * página detalhada de cada item
  * página para criar itens
  * página de atualização de itens (um usuário só pode alterar item que lhe pertence) (precisa corrigir update de foto)
  * página para deletar itens

  > * Atualmente todas as views utilizam a chamada Class Based Views
  > * templates html ficam separados por uma pasta na raiz chamada 'templates' com subpastas para partials e cada aplicatico com cada pasta de partials
  > * arquivos static ficam em outra pasta na raiz chamada 'static' subdividida de acordo com os arquivos
  > * imagens de produtos ficam salvos dentro de 'media' na raiz do projeto, separados por ano - mês - dia
  > * os aplicativos ficam guardados dentro da pasta 'apps' na raiz do programa
  > * tests serão implementados assim que finalizar 100% dos dois apps
