from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Usuário',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar a Senha',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Criar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Usuário já existente. Por favor, escolher outro diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já utilizado. Por favor, escolher outro diferente.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Acessar')

class UpdateAccountForm(FlaskForm):
    username = StringField('Usuário',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Atualizar foto.', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Usuário já existente. Por favor, escolher outro diferente.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email já utilizado. Por favor, escolher outro diferente.')

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Texto', validators=[DataRequired()])
    submit = SubmitField('Postar')
    

class SugestForm(FlaskForm):
    username = StringField('Nome',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    textoSug = TextAreaField('Escreva aqui suas sugestões',
                           validators=[DataRequired(), Length(min=2, max=500)])
    
    submit = SubmitField('Enviar')


class PostaAnuncioForm(FlaskForm):
    foto = FileField('Foto', validators=[FileRequired()])
    titulo = StringField('Título', validators=[DataRequired()])
    texto = StringField('Texto do Anúncio', validators=[DataRequired()])
    dt_inclusao = StringField('Data da Inclusão', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    nomeAnunciante = StringField('Nome do Anunciante', validators=[DataRequired()])
    telcont = StringField('Telefone para Contato', validators=[DataRequired()])
    submit = SubmitField('Postar')
    

class DesabilitaAnuncioForm(FlaskForm):
    numero = StringField('Número do Anúncio', validators=[DataRequired()])
    submit = SubmitField('Desabilitar')


   # def validate_username(self, username):
   #     user = User.query.filter_by(username=username.data).first()
   #     if user:
   #         raise ValidationError('That username is taken. Please choose a different one.')

   # def validate_email(self, email):
   #     user = User.query.filter_by(email=email.data).first()
   #     if user:
   #         raise ValidationError('That email is taken. Please choose a different one.')
