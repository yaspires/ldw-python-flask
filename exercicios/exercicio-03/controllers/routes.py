from flask import render_template, request, redirect, url_for
from models.database import db, Movie, Filmaker
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
            url = f"https://api.themoviedb.org/3/movie/{id}?api_key={tmdb_api_key}&language=pt-BR"
            response = urllib.request.urlopen(url)
            data = response.read()
            movieInfo = json.loads(data)
            if movieInfo.get('id'):
                return render_template('movieinfo.html', movieInfo=movieInfo)
            else:
                return f"Filme com a ID {id} não foi encontrado"
        else:
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=pt-BR&page=1"
            response = urllib.request.urlopen(url)
            data = response.read()
            payload = json.loads(data)
            moviesList = payload.get('results', [])
            return render_template('apimovies.html', moviesList=moviesList)

    @app.route('/movies/estoque', methods=['GET', 'POST'])
    @app.route('/movies/estoque/delete/<int:id>')
    def moviesEstoque(id=None):
        if id:
            movie = Movie.query.get(id)
            db.session.delete(movie)
            db.session.commit()
            return redirect(url_for('moviesEstoque'))
        if request.method == 'POST':
            newmovie = Movie(request.form['titulo'], request.form['ano'], request.form['genero'],
                             request.form['preco'], request.form['quantidade'], request.form['filmaker'])
            db.session.add(newmovie)
            db.session.commit()
            return redirect(url_for('moviesEstoque'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 3
            movies_page = Movie.query.paginate(page=page, per_page=per_page)
            filmakers = Filmaker.query.all()

            return render_template('moviesestoque.html', moviesestoque=movies_page, filmakers=filmakers)

    @app.route('/movies/edit/<int:id>', methods=['GET', 'POST'])
    def movieEdit(id):
        m = Movie.query.get(id)
        if request.method == 'POST':
            m.titulo = request.form['titulo']
            m.ano = request.form['ano']
            m.genero = request.form['genero']
            m.preco = request.form['preco']
            m.quantidade = request.form['quantidade']
            m.filmaker_id = request.form['filmaker']
            
            db.session.commit()
            return redirect(url_for('moviesEstoque'))
        filmakers = Filmaker.query.all()
        return render_template('editmovie.html', m=m, filmakers=filmakers)

    @app.route('/filmakers/lista', methods=['GET', 'POST'])
    @app.route('/filmakers/lista/delete/<int:id>')
    def filmakersEstoque(id=None):
        if id:
            filmaker = Filmaker.query.get(id)
            db.session.delete(filmaker)
            db.session.commit()
            return redirect(url_for('filmakersEstoque'))
        if request.method == 'POST':
            newfilmaker = Filmaker(
                request.form['nome'], request.form['idade'], request.form['premios'])
            db.session.add(newfilmaker)
            db.session.commit()
            return redirect(url_for('filmakersEstoque'))
        else:
            page = request.args.get('page', 1, type=int)
          
            per_page = 3
            filmakers_page = Filmaker.query.paginate(
                page=page, per_page=per_page)
            return render_template('filmakerlist.html', filmakersestoque=filmakers_page)


    @app.route('/filmakers/edit/<int:id>', methods=['GET', 'POST'])
    def filmakerEdit(id):
        filmaker = Filmaker.query.get(id)
        if request.method == 'POST':
            filmaker.nome = request.form['nome']
            filmaker.idade = request.form['idade']
            filmaker.premios = request.form['premios']
            db.session.commit()
            return redirect(url_for('filmakersEstoque'))
        return render_template('editfilmaker.html', filmaker=filmaker)