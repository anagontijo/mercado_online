import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AddProductForm, AddToCartForm, RemoveFromCartForm, PaymentForm, AddToStockForm
from flaskblog.models import User, Post, Product, Order
from flask_login import login_user, current_user, logout_user, login_required
from classes import Carrinho
import datetime

actual_shopcart = Carrinho()

def is_adm():
    is_adm = False
    if current_user.is_authenticated:
        if current_user.username == 'admin':
            is_adm = True
    return is_adm

def calculate_time(itens):
    tempo = 5 * sum(list(itens.values()))
    for item in list(itens.keys()):
        tempo += itens[item]/12
    return tempo

# Rota para a página home do sistema
@app.route("/")
@app.route("/home")
def home():
    #posts = Post.query.all()
    products = Product.query.all()
    return render_template("home.html", products=products, is_adm = is_adm())

# Rota para a página about do sistema
@app.route("/about")
def about():
    return render_template("about.html", title='About')

# Rota para o registro de novo usuário
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'Success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# Rota para o login do usuário
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log In Unsuccessful. Please check e-mail and password', 'danger')

    return render_template('login.html', title='Login', form=form)

# Rota para logout
@app.route("/logout")
def logout():
    logout_user()
    actual_shopcart.esvaziar()
    return redirect(url_for('home'))

# Função para salvar foto carregada
def save_picture(form_picture,path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, path, picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# Rota para a visualização da conta do usuário
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,'static/profile_pics')
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form,is_adm = is_adm())

# Rota para criação de novo post
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# Adiciona um novo produto ao bd via formulário
@app.route("/add_new_product", methods=['GET', 'POST'])
@login_required
def add_new_product():
    if current_user.username != 'admin':
        abort(403)
    form = AddProductForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.image_file.data,'static/product_pics')
        product = Product(name=form.name.data, price=form.price.data, description=form.description.data, stock = form.stock.data, image_file = picture_file)
        db.session.add(product)
        db.session.commit()
        flash('Your product has been added.', 'success')
        return redirect(url_for('home'))
    return render_template('add_product.html', title='Add Product', form=form, legend='Add Product',is_adm = is_adm())

# Rota da página de cada post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# Rota da página de cada produto
@app.route("/product/<int:product_id>", methods=['GET', 'POST'])
@login_required
def product(product_id):
    if is_adm():
        form = AddToStockForm()
        product = Product.query.get_or_404(product_id)

        if form.validate_on_submit():
            flash('Os produtos foram adicionados ao estoque.', 'success')
            product.stock += form.quantity.data
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print('form errado')

        return render_template('product.html', title=product.name, form=form, product=product, available=product.stock,is_adm = is_adm())

    else:
        form = AddToCartForm()
        product = Product.query.get_or_404(product_id)

        available = product.stock - actual_shopcart.itens[product_id]

        if form.validate_on_submit() and form.quantity.data <= available:
            flash('O produto foi adicionado ao carrinho.', 'success')
            actual_shopcart.adicionar_produto(product.id, form.quantity.data, product.price)
            return redirect(url_for('home'))
        elif form.validate_on_submit():
            flash('Quantidade acima do estoque', 'warning')
        else:
            print('form errado')

        return render_template('product.html', title=product.name, form=form, product=product, available=available,is_adm = is_adm())

@app.route("/shopcart", methods=['GET', 'POST'])
def shopcart():
    shopcart_products = []
    form = RemoveFromCartForm()
    for item in list(actual_shopcart.itens.keys()):
        shopcart_products.append(Product.query.get_or_404(item))
    full_price = "{:.2f}".format(actual_shopcart.preco_total)

    return render_template('shopcart.html', title="Carrinho", form= form, shopcart=actual_shopcart, products=shopcart_products, full_price=full_price,is_adm = is_adm())

@app.route("/shopcart/remove/<int:product_id>/<float:price>", methods=['GET', 'POST'])
def remove(product_id,price):
    print('removing')
    actual_shopcart.remover_produto(product_id,price)
    return shopcart()


# Rota de pagamento da compra
@app.route("/payment", methods=['GET', 'POST'])
@login_required
def payment():
    shopcart_products = []
    form = PaymentForm()
    for item in list(actual_shopcart.itens.keys()):
        shopcart_products.append(Product.query.get_or_404(item))
    full_price = "{:.2f}".format(actual_shopcart.preco_total)

    if form.validate_on_submit():
        flash('Seu pagamento está sendo processado.', 'success')
        time = datetime.datetime.now()
        for item in actual_shopcart.itens.keys():
            actual_product = Product.query.get_or_404(item)
            actual_product.stock -= actual_shopcart.itens[item]
            db.session.commit()

        ready = time + datetime.timedelta(0, calculate_time(actual_shopcart.itens))
        full_price = "{:.2f}".format(actual_shopcart.preco_total)
        order = Order(email=current_user.email, price=full_price,
                        order_time=time, order_ready=ready)
        db.session.add(order)
        actual_shopcart.esvaziar()
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('payment.html',title='Pagamento', full_price=full_price, form=form,is_adm = is_adm())

# Rota de update de post de usuário
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# Rota de delete de post de usuário
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

@app.route("/orders", methods=['GET', 'POST'])
@login_required
def orders():
    if is_adm():
        orders_list = Order.query.all()
        total = "{:.2f}".format(sum([float(a.price) for a in orders_list]))
    else:
        orders_list = Order.query.filter_by(email=current_user.email)
        total = 0
    return render_template('orders.html', total=total, title='Pedidos', orders=orders_list, is_adm = is_adm())
