import unittest
import sys
import os
sys.path.insert(1, os.path.abspath('')[:-16])
from flaskblog import app, db
#from contextlib import contextmanager
#from io import StringIO
 
 
TEST_DB = 'test.db'
 
class BasicTests(unittest.TestCase):
 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        self.assertEqual(app.debug, False)
 
    def tearDown(self):
        db.drop_all()
        pass
 
 
    def test_home_page(self):
        tester = app.test_client(self)
        response = tester.get('/home', follow_redirects=True, content_type = 'html/text')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertTrue(b'Register' in response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertTrue(b'Log In' in response.data)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_accountt_page(self):
        response = self.app.get('/account', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_new_product_page(self):
        response = self.app.get('/add_new_product', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_shopcart_page(self):
        response = self.app.get('/shopcart', follow_redirects=True)
        self.assertTrue(b'Carrinho' in response.data)
        self.assertEqual(response.status_code, 200)

    def test_payment_page(self):
        response = self.app.get('/payment', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_orders_page(self):
        response = self.app.get('/orders', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

 
if __name__ == "__main__":
    unittest.main()