from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer,nullable=False)
    image_file = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False, default = 'Descrição do produto.')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}', {self.stock})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    order_ready = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __repr__(self):
        return f"Order('{self.email}', '{self.price}', {self.order_time}, {self.order_ready})"
