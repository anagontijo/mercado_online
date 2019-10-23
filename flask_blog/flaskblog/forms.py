from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Corfirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nome de usuário já em uso, por favor escolha outro')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já em uso, por favor escolha outro')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Nome', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Nome de usuário já em uso, por favor escolha outro')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('E-mail já em uso, por favor escolha outro')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AddProductForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    price = DecimalField("Preço", validators=[DataRequired()])
    description = StringField('Descrição', validators=[])
    stock = IntegerField('Estoque', validators=[DataRequired()])
    image_file = FileField('Imagem do Produto', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Adicionar')

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0,message="Quantidade inválida.")])
    submit = SubmitField('Adicionar ao carrinho')

class AddToStockForm(FlaskForm):
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0,message="Quantidade inválida.")])
    submit = SubmitField('Adicionar ao Estoque')

class RemoveFromCartForm(FlaskForm):
    submit = SubmitField('Remover')

class PaymentForm(FlaskForm):
    nome_do_titular = StringField('Nome do Titular', validators=[DataRequired()])
    numero_do_cartao = StringField('Número do Cartão', validators=[DataRequired()])
    cvv = StringField('Código de Segurança', validators=[DataRequired()])
    submit = SubmitField('Realizar Pagamento')
