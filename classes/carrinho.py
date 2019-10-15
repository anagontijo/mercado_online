from collections import defaultdict

class Carrinho():
    def __init__(self, catalogo):
        self.itens = defaultdict(int)
        self.preco_total = 0
        self.catalogo = catalogo

    def adicionar_produto(self, cod_produto, qtd):
        if cod_produto in self.itens.keys():
            total = qtd + self.itens[cod_produto]
        else:
            total = qtd
        if self.catalogo.verifica_estoque(cod_produto) - total >= 0:
            self.itens[cod_produto] += qtd
            self.preco_total += self.catalogo.verifica_preco(cod_produto)*qtd
        else:
            raise stockException("Estoque insuficiente.")

    def remover_produto(self, cod_produto, qtd):
        if cod_produto in self.itens.keys():
            qtd = min(qtd,self.itens[cod_produto])
            self.itens[cod_produto] -= qtd
            self.preco_total -= self.catalogo.verifica_preco(cod_produto)*qtd
        else:
            raise cartException("Este produto não está no carrinho.")

    def esvaziar(self):
        self.itens = defaultdict(int)
        self.preco_total = 0

    def finaliza_compra(self, save=True):
        for cod in self.itens.keys():
            self.catalogo.remover_produto(cod, self.itens[cod])
        preco = self.preco_total
        self.esvaziar()
        if save:
            self.catalogo.salvar_mudancas()
        return preco

class stockException(Exception):
    pass

class cartException(Exception):
    pass
