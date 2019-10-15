import unittest
import sys
import os
sys.path.insert(1, os.path.abspath('')[:-10])
import classes

class TestCarrinho(unittest.TestCase):
    def setUp(self):
        self.shopcarts = []
        # Preço do produto padrão a ser testado
        self.aux_price = 7.09
        self.cat = classes.Catalogo()
        itens = [{1:1,2:2,3:3},{10:1,20:2,30:3},{10:1,30:2,50:3}]
        precos = [20 + (2 * 3.5) + (3 * 3.8),
                  13.9 + (2 * 2.53) + (3 * 7.09),
                  13.9 + (2 * 7.09) + (3 * 4.19)]
        for i in range(3):
            self.shopcarts.append(classes.Carrinho(self.cat))
            self.shopcarts[i].itens = itens[i]
            self.shopcarts[i].preco_total = precos[i]

    def test_adicionar_produto(self):
        results = [1,4,3]
        # Teste quando há estoque
        for i,cart in enumerate(self.shopcarts):
            price_before = cart.preco_total
            cart.adicionar_produto(cod_produto=30,qtd=1)
            self.assertEqual(cart.itens[30],results[i])
            self.assertEqual(cart.preco_total, price_before + self.aux_price)
        self.assertRaises("Estoque insuficiente.",
                          self.shopcarts[0].adicionar_estoque(cod_produto=52,
                                                              qtd=101))

    def test_remover_produto(self):
        results = [0,3,2]
        self.assertRaises("Este produto não está no carrinho.", self.shopcarts[0].remover_produto(cod_produto=30, qtd=1))
        for i, cart in enumerate(self.shopcarts[1:]):
            for j in range(5):
                price_before = cart.preco_total
                cart.remover_produto(cod_produto=30, qtd=j)
                self.assertEqual(cart.itens[30], max(results[i]-j,0))
                self.assertEqual(cart.preco_total, price_before -
                                 (max(results[i]-j,0)*self.aux_price))

    def test_esvaziar(self):
        for cart in self.shopcarts:
            cart.esvaziar()
            self.assertEqual(len(cart.itens.keys()),0)
            self.assertEqual(cart.preco_total, 0)

    def test_finaliza_compra(self):
        for cart in self.shopcarts:
            cods = cart.itens.keys()
            qtds = cart.itens.values()
            qtd_1 = self.cat.verifica_estoque(cods[0])
            qtd_2 = self.cat.verifica_estoque(cods[1])
            qtd_3 = self.cat.verifica_estoque(cods[2])
            price = cart.preco_total

            result = cart.finaliza_compra(save=False)

            self.assertEqual(qtd_1, self.cat.verifica_estoque(cods[0]) +
                             qtds[0])
            self.assertEqual(qtd_1, self.cat.verifica_estoque(cods[1]) +
                             qtds[1])
            self.assertEqual(qtd_1, self.cat.verifica_estoque(cods[2]) +
                             qtds[2])
            self.assertEqual(price, result)


if __name__ == '__main__':
    unittest.main()
