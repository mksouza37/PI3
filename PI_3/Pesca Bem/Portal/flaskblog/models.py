from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    postsbl = db.relationship('Postblog', backref='author', lazy=True)

    def __repr__(self):

        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):

        return f"Post('{self.title}', '{self.date_posted}')"


class Postblog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):

        return f"Postblog('{self.title}', '{self.date_posted}')"
     
class empresas(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    cnpj = db.Column(db.Text, nullable=False)
    cidade = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Text, nullable=False)
    ramo = db.Column(db.Text, nullable=False)
    conduta = db.Column(db.Text, nullable=False)
    

class Legislacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.Integer, primary_key=False)
    siglaTipo = db.Column(db.Text, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    ementa = db.Column(db.Text, nullable=False)
    uri = db.Column(db.Text, nullable=False)


class Noticias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataPub = db.Column(db.Text, primary_key=False)
    titulo = db.Column(db.Text, primary_key=False)
    link = db.Column(db.Text, primary_key=False)
    

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foto = db.Column(db.LargeBinary, nullable=False)
    titulo = db.Column(db.Text, nullable=False)
    texto = db.Column(db.Text, nullable=False)
    dt_inclusao = db.Column(db.Text, nullable=False)
    cidade = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Text, nullable=False)
    nomeAnunciante = db.Column(db.Text, nullable=False)
    telcont = db.Column(db.Text, nullable=False)
    usuarioCad = db.Column(db.Text, nullable=False)
    statusvigencia = db.Column(db.Text, nullable=False)

    


    
    
