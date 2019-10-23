from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That e-mail is taken, please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That e-mail is taken, please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    description = StringField('Description', validators=[])
    stock = IntegerField('Stock', validators=[DataRequired()])
    image_file = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0,max=100,message="Quantidade inválida.")])
    submit = SubmitField('Adicionar ao carrinho')

class AddToStockForm(FlaskForm):
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0,message="Quantidade inválida.")])
    submit = SubmitField('Adicionar ao estoque')

class RemoveFromCartForm(FlaskForm):
    submit = SubmitField('Remover')

class PaymentForm(FlaskForm):
    nome_do_titular = StringField('Nome do Titular', validators=[DataRequired()])
    numero_do_cartao = StringField('Número do Cartão', validators=[DataRequired()])
    cvv = StringField('Código de Segurança', validators=[DataRequired()])
    submit = SubmitField('Realizar Pagamento')
