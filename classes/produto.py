class Produto():
    def __init__(self, codigo, nome, preco, estoque):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def adicionar_estoque(self, qtd):
        self.estoque += qtd

    def remover_estoque(self, qtd):
        if self.estoque - qtd >= 0:
            self.estoque -= qtd
        else:
            self.estoque = 0

    def mudar_preco(self, novo_preco):
        self.preco = novo_preco