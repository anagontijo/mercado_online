import BD
import classes

catalogo = BD.Catalogo()
carrinho = classes.Carrinho(catalogo)

for item in catalogo.produtos:
    carrinho.adicionar_produto(item.codigo, 10)
    # Para exception de estoque:
    # carrinho.adicionar_produto(item.codigo, 20)

print(carrinho.itens)
print(carrinho.preco_total)
print(carrinho.finaliza_compra())
