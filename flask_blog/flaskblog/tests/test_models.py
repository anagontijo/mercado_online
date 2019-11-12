import unittest
import sys
import os
from collections import defaultdict
from datetime import datetime, timedelta
sys.path.insert(1, os.path.abspath('')[:-16])
from flaskblog import db, models
from contextlib import contextmanager
from io import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestModels(unittest.TestCase):
    def setUp(self):
        self.product = models.Product(name="Teste", price=12.34,
                          description="Teste teste teste",
                          stock = 5678, image_file = "teste.jpg")
        self.user = models.User(username="Teste", email="Teste@gmail.com", password="teste")
        self.order = models.Order(email="Teste@gmail.com", price=300)

    def test_product(self):
        with captured_output() as (out, err):
            print(self.product)
        output = out.getvalue().strip()
        self.assertEqual(output, "Product('Teste', '12.34', 5678)")
        db.session.add(self.product)
        product_in_db = models.Product.query.filter_by(name="Teste").first()
        self.assertTrue(product_in_db.name == self.product.name)
        self.assertTrue(product_in_db.stock == self.product.stock)
        self.assertTrue(product_in_db.price == self.product.price)
        self.assertTrue(product_in_db.description == self.product.description)
        self.assertTrue(product_in_db.image_file == self.product.image_file)


    def test_user(self):
        with captured_output() as (out, err):
            print(self.user)
        output = out.getvalue().strip()
        self.assertEqual(output, "User('Teste', 'Teste@gmail.com', 'None')")
        db.session.add(self.user)
        user_in_db = models.User.query.filter_by(email='Teste@gmail.com').first()
        self.assertTrue(isinstance(user_in_db.id, int))
        self.assertTrue(user_in_db.username == self.user.username)
        self.assertTrue(user_in_db.email == self.user.email)
        self.assertTrue(user_in_db.password == self.user.password)
        self.assertTrue(user_in_db.image_file == "default.jpg")
        with captured_output() as (out, err):
            print(user_in_db)
        output = out.getvalue().strip()
        self.assertEqual(output, "User('Teste', 'Teste@gmail.com', 'default.jpg')")


    def test_order(self):
        with captured_output() as (out, err):
            print(self.order)
        output = out.getvalue().strip()
        self.assertEqual(output, "Order('Teste@gmail.com', '300', None, None)")
        db.session.add(self.order)
        od_time = datetime.utcnow()
        od_ready = datetime.utcnow()
        order_in_db = models.Order.query.filter_by(email='Teste@gmail.com').first()
        self.assertTrue(order_in_db.email == self.order.email)
        self.assertTrue(order_in_db.price == self.order.price)
        self.assertTrue(order_in_db.order_time - od_time < timedelta(1e-5))
        self.assertTrue(order_in_db.order_ready - od_ready < timedelta(1e-5))
        with captured_output() as (out, err):
            print(order_in_db)
        output = out.getvalue().strip()
        self.assertEqual(output, "Order('Teste@gmail.com', '300', "+str(order_in_db.order_time)+", "+str(order_in_db.order_ready)+")")


if __name__ == '__main__':
    unittest.main()
