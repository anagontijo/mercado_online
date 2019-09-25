# Mercado Online
## Classes
### Produto  
A classe produto é a classe em python para organização dos produtos do catálogo. Os parâmetros da classe são todos os atributos.

#### Atributos

* __Código (_int_)__   
  Uma chave única para identificação do produto.
* __Nome (_string_)__  
  Nome comercial do produto.
* __Preço (_float_)__  
  Preço do produto
* __Estoque (_int_)__  
  Quantidade de unidades do produto no estoque.
  
#### Métodos
 
* __adicionar_estoque__

* __remover_estoque__

* __mudar_preco__

### Carrinho  
A classe carrinho é a classe em python para gerenciamento do carrinho de compras em uma compra. O único parâmetro que esta classe recebe é o catálogo a ser utilizado.

#### Atributos

* __Itens (_dict_{int:int})__
  Dicionário que relaciona os códigos dos produtos que estão no carrinho com suas quantidades. 

* __Preço Total (_float_)__
  O preço atual total do carrinho com a lista de itens atual. 

* __Catálogo (_Catalogo_)__
  O catálogo que está sendo utilizado nesta compra.

#### Métodos

* __adicionar_produto (código, quantidade)__  
  Adiciona a quantidade específica do produto relativo ao código ao carrinho caso essa quantidade esteja disponível no catálogo. 

* __remover_produto (código, quantidade)__  
  Remove a quantidade específica do produto e deleta a chave do dicionário caso a quantidade fique igual a 0.
  
* __esvaziar__  
  Reinicia o dicionário de itens e o preço total.

* __finaliza_compra__  
  Remove as quantidades dos itens que estão no carrinho do banco de dados e retorna o preço final.
  
### Catalogo  
A classe para carregar o catálogo do banco de dados e gerenciar este.

#### Atributos  

* __Produtos (_list_[Produto])__  
  Lista dos produtos no banco de dados, armazenados em objetos da classe Produto.
  
* __Códigos (_list_[int])__
  Lista dos códigos dos produtos no banco de dados, para facilitar verificação de existência do código.
  
#### Métodos

* __adicionar_produto(novo, quantidade, código, preço=None,nome=None)__
  Adiciona novo produto (com novo código) caso o parâmetro "novo" seja True, nesse caso os parâmetros preço e nome devem ser passados. Caso o parâmetro "novo" seja False, adiciona a quantidade ao estoque do produto.
  
* __remover_produto(código, quantidade=None)__
  Remove o produto do código completamente do catálogo caso a "quantidade" seja None, caso a quantidade seja passada essa quantidade será retirada do estoque, ou o estoque será zerado caso a quantidade seja maior que o estoque.
  
* __verifica_estoque(código)__
  Retorna qual é a quantidade de itens no estoque (retorna -1 caso o código não exista no catálogo)
  
* __verifica_preco(código)__
  Retorna o preço do produto no catálogo (retorna -1 caso o código não exista no catálogo)
  
* __modificar_preco(código, preco)__
  Modifica o preço do produto relativo ao código para o preço passado.
  
* __visualizar_imagem(código)__
  Exibe a imagem relacionada ao código do produto no banco de dados.
  
* __salvar_mudanças__
  Salva as mudanças que foram feitas ao banco de dados.
  
### Usuarios
A classe para carregar os usuarios do banco de dados e gerenciar estes.

#### Atributos
* __gerentes (_dict_{string:string})__  
  Dicionário de usuários com permissões de gerente com chaves relativas ao login do usuário e valor relativo a senha.
* __clientes (_dict_{string:string})__  
  Dicionário de usuários com permissões de cliente com chaves relativas ao login do usuário e valor relativo a senha.
* __logins (_list_[string])__  
  Lista contendo os logins utilizados para facilitar verificação de logins presentes no banco de dados.
