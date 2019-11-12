import unittest
import sys
import os
from collections import defaultdict
sys.path.insert(1, os.path.abspath('')[:-16])
import classes

class TestCarrinho(unittest.TestCase):
    def setUp(self):
        self.shopcarts = []
        # Preço do produto padrão a ser testado
        self.aux_price = 7.09
        itens = [defaultdict(int), defaultdict(int), defaultdict(int)]
        itens_aux = [{(1,1),(2,2),(3,3)},{(10,1),(20,2),(30,3)},[(10,1),(30,2),(50,3)]];
        for i, list in enumerate(itens_aux):
            for item in list:
                itens[i][item[0]] = item[1]
        self.prices = {1:20, 2:3.5, 3:3.8, 10:13.9, 20:2.53, 30:7.09, 50:4.19}
        precos = [20 + (2 * 3.5) + (3 * 3.8),
                  13.9 + (2 * 2.53) + (3 * 7.09),
                  13.9 + (2 * 7.09) + (3 * 4.19)]
        for i in range(3):
            self.shopcarts.append(classes.Carrinho())
            self.shopcarts[i].itens = itens[i]
            self.shopcarts[i].preco_total = precos[i]

    def test_adicionar_produto(self):
        results = [1,4,3]
        for i,cart in enumerate(self.shopcarts):
            price_before = cart.preco_total
            cart.adicionar_produto(id=30,qtd=1,price=self.prices[30])
            self.assertEqual(cart.itens[30],results[i])
            self.assertEqual(cart.preco_total, price_before + self.aux_price)

    def test_remover_produto(self):
        results = [3,2]
        for i, cart in enumerate(self.shopcarts[1:]):
            price_before = cart.preco_total
            cart.remover_produto(id=30, price=self.prices[30])
            self.assertTrue(30 not in cart.itens.keys())
            self.assertEqual(cart.preco_total, price_before -\
                        results[i]*self.aux_price)
            cart.itens[30] = results[i]
            cart.preco_total += results[i]*self.aux_price

    def test_esvaziar(self):
        for cart in self.shopcarts:
            cart.esvaziar()
            self.assertEqual(len(cart.itens.keys()),0)
            self.assertEqual(cart.preco_total, 0)

if __name__ == '__main__':
    unittest.main()
