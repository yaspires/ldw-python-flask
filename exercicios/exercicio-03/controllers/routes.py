from flask import render_template, request, redirect, url_for
from models.database import db, Game, Console
import urllib
import json

def init_app(app):
    filmes = ['Ilha do medo', 'Os oito odiados', 'Kill bill', 'Pulp fiction']
    filmakerList = [{'Nome': 'Tim Burtom', 'Idade': 67, 'Premios': 'Leão de ouro, Empire award ...'}]
    
    
    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/diretor', methods=['GET', 'POST'])
    def diretor():
        nome = 'Quentin Tarantino'
        idade = 62
        premios = 'Oscar, Globo de ouro, Cavalo de bronze ...'
        destaque = {'Titulo' : 'Django livre', 'ano': 2012, 'genero' : 'Faroeste/Ação'}

        if request.method == 'POST':
            if request.form.get('filme'):
                filmes.append(request.form.get('filme'))
                return redirect(url_for('diretor'))
        
        return render_template('diretor.html', nome=nome, idade=idade, premios=premios, filmes=filmes, destaque=destaque)
    
    
    @app.route('/newFilmaker', methods=['GET', 'POST'])
    def newFilmaker():
        if request.method == 'POST':
            if request.form.get('nome') and request.form.get('idade') and request.form.get('premios'):
                filmakerList.append({'Nome': request.form.get('nome'), 'Idade': request.form.get('idade'), 'Premios' : request.form.get('premios')})
                return redirect(url_for('newFilmaker'))
                
        return render_template('newFilmaker.html', filmakerList=filmakerList)
    
    @app.route('/apimovies', methods=['GET', 'POST'])
    @app.route('/apimovies/<id>', methods=['GET', 'POST'])
    def apimovies(id=None):
        tmdb_api_key = '24d9c59f672e2e463038398486f0b532'
        if id:
            # Detalhes na TMDb por ID TMDb
            url = f"https://api.themoviedb.org/3/movie/{id}?api_key={tmdb_api_key}&language=pt-BR"
            response = urllib.request.urlopen(url)
            data = response.read()
            movieInfo = json.loads(data)
            if movieInfo.get('id'):
                return render_template('movieinfo.html', movieInfo=movieInfo)
            else:
                return f"Filme com a ID {id} não foi encontrado"
        else:
            # Catálogo popular na TMDb
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=pt-BR&page=1"
            response = urllib.request.urlopen(url)
            data = response.read()
            payload = json.loads(data)
            moviesList = payload.get('results', [])
            return render_template('apimovies.html', moviesList=moviesList)
    