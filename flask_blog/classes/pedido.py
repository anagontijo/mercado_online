from collections import defaultdict

class Pedido():
    def __init__(self, comprador, carrinho):
        self.itens = carrinho.itens
        self.preco = carrinho.preco_total
        self.conta = comprador
        self.tempo = self.calcula_tempo()

    def calcula_tempo(self):
        tempo = 5 * sum(list(self.itens.values()))
        for item in list(self.itens.keys()):
            tempo += self.itens[item]/12
        return tempo
