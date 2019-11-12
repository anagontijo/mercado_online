from collections import defaultdict

class Carrinho():
    def __init__(self):
        self.itens = defaultdict(int)
        self.preco_total = 0

    def adicionar_produto(self, id, qtd, price):
        self.itens[id] += qtd
        self.preco_total += qtd*price

    def remover_produto(self, id, price):
        qtd = self.itens[id]
        self.preco_total -= qtd * price
        self.itens.pop(id)

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
