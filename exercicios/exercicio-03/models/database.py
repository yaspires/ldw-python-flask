from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Filmaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)
    premios = db.Column(db.String(255))

    def __init__(self, nome, idade, premios):
        self.nome = nome
        self.idade = idade
        self.premios = premios


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    ano = db.Column(db.Integer)
    genero = db.Column(db.String(150))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    filmaker_id = db.Column(db.Integer, db.ForeignKey('filmaker.id'))
    filmaker = db.relationship('Filmaker', backref=db.backref('movies', lazy=True))

    def __init__(self, titulo, ano, genero, preco, quantidade, filmaker_id):
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.preco = preco
        self.quantidade = quantidade
        self.filmaker_id = filmaker_id
