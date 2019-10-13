import unittest
import sys
import os
sys.path.insert(1, os.path.abspath('')[:-10])
import classes

class TestProduto(unittest.TestCase):
    def setUp(self):
        self.product_examples = []
        self.product_examples.append(classes.Produto(codigo=1,nome="Carne",
                                                preco=9.99, estoque=10))
        self.product_examples.append(classes.Produto(codigo=2,nome="Arroz",
                                                preco=2.50, estoque=0))
        self.product_examples.append(classes.Produto(codigo=3,nome="Feijão",
                                                preco=3.75, estoque=20))

    def test_adicionar_estoque(self):
        quantities = [20,30,10]
        for index, product in enumerate(self.product_examples):
            product.adicionar_estoque(quantities[index])
            self.assertEqual(product.estoque,30)

    def test_remover_estoque(self):
        expected_result = [0,0,10]
        for index, product in enumerate(self.product_examples):
            product.remover_estoque(10)
            self.assertEqual(product.estoque,expected_result[index])

    def test_mudar_preco(self):
        new_price = 1.99
        for product in self.product_examples:
            product.mudar_preco(new_price)
            self.assertEqual(product.preco, new_price)

if __name__ == '__main__':
    unittest.main()
