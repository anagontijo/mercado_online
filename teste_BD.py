import BD
import classes

catalogo = BD.Catalogo()

print(catalogo.produtos[0].estoque, catalogo.produtos[0].preco)

catalogo.visualizar_imagem(1)
catalogo.remover_produto(qtd=10, codigo=1)
catalogo.modificar_preco(codigo=1,preco=20.0)

catalogo.salvar_mudancas()

print(catalogo.produtos[0].estoque, catalogo.produtos[0].preco)

usuarios = BD.Usuarios()

print(usuarios.gerentes, usuarios.clientes)

usuarios.remover_usuario("outrapessoa")
usuarios.adicionar_usuario("pessoa","0123","C")
print(usuarios.tipo_do_usuario("anagontijo"))

print(usuarios.gerentes, usuarios.clientes)
