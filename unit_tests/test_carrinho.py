import unittest
import sys
import os
from collections import defaultdict
sys.path.insert(1, os.path.abspath('')[:-10])
import classes, BD

class TestCarrinho(unittest.TestCase):
    def setUp(self):
        self.shopcarts = []
        # Preço do produto padrão a ser testado
        self.aux_price = 7.09
        self.cat = BD.Catalogo()
        itens = [defaultdict(int), defaultdict(int), defaultdict(int)]
        itens_aux = [{(1,1),(2,2),(3,3)},{(10,1),(20,2),(30,3)},[(10,1),(30,2),(50,3)]];
        for i, list in enumerate(itens_aux):
            for item in list:
                itens[i][item[0]] = item[1]
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
        self.assertRaises(classes.stockException,
                          self.shopcarts[0].adicionar_produto,cod_produto=52,
                                                              qtd=101)

    def test_remover_produto(self):
        results = [3,2]
        self.assertRaises(classes.cartException, self.shopcarts[0].remover_produto,cod_produto=30, qtd=1)
        for i, cart in enumerate(self.shopcarts[1:]):
            for j in range(5):
                price_before = cart.preco_total
                cart.remover_produto(cod_produto=30, qtd=j)
                self.assertEqual(cart.itens[30], max(results[i]-j,0))
                self.assertEqual(cart.preco_total, price_before -
                                 (min(j,results[i])*self.aux_price))
                cart.itens[30] += min(j,results[i])
                cart.preco_total += min(j,results[i])*self.aux_price

    def test_esvaziar(self):
        for cart in self.shopcarts:
            cart.esvaziar()
            self.assertEqual(len(cart.itens.keys()),0)
            self.assertEqual(cart.preco_total, 0)

    def test_finaliza_compra(self):
        for cart in self.shopcarts:
            cods = list(cart.itens.keys())
            qtds = list(cart.itens.values())
            qtd_1 = self.cat.verifica_estoque(cods[0])
            qtd_2 = self.cat.verifica_estoque(cods[1])
            qtd_3 = self.cat.verifica_estoque(cods[2])
            price = cart.preco_total

            result = cart.finaliza_compra(save=False)

            self.assertEqual(qtd_1, self.cat.verifica_estoque(cods[0]) +
                             qtds[0])
            self.assertEqual(qtd_2, self.cat.verifica_estoque(cods[1]) +
                             qtds[1])
            self.assertEqual(qtd_3, self.cat.verifica_estoque(cods[2]) +
                             qtds[2])
            self.assertEqual(price, result)


if __name__ == '__main__':
    unittest.main()
