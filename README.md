# Django_Eshop_Estudo
> Status atual (02/10/2021) - Finalizado

 O objetivo deste projeto foi criar um app para treinar e aprender mais a fundo a ferramenta Django junto com CSS, JavaScript, MySQL. A duração do projeto, feito durante meu tempo livre, foi de 6 mêses.

Criado três aplicativos: user_app, loja_app e cart_app

user_app gerencia: 
  * Login do user
  * Cadastro do user
  * Logoff do user
  * Página de info do user (o user só recebe informação a respeito dele mesmo)
  * Página de atualização de info do user (o usuário só consegue alterar as informações dele mesmo)

loja_app gerencia:
  * Listagem de itens (página index)
  * Listagem de itens do user
  * página detalhada de cada item
  * página para criar itens
  * página de atualização de itens (um usuário só pode alterar item que lhe pertence)
  * página para deletar itens (o usuário só pode deletar itens que lhe pertence)

cart_app gerencia:
  * Listagem de itens no carrinho
  * Remover itens do carrinho
  * Adicionar itens no carrinho

  > * Utilizado o princípio DRY (Don't repeat yourself)
  > * Praticamente todas as views utilizam o chamado de Class Based Views
  > * templates html ficam separados por uma pasta na raiz chamada 'templates' com subpastas para aplicativos e partials
  > * arquivos static ficam em outra pasta na raiz chamada 'static' subdividida de acordo com os arquivos
  > * imagens de produtos ficam salvos dentro de 'media' na raiz do projeto, separados por ano - mês - dia
  > * os aplicativos ficam guardados dentro da pasta 'apps' na raiz do programa
  > * todos os testes unitários de todos os apps já foram implementados
