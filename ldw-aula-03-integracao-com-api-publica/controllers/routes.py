from flask import render_template, request, redirect, url_for
import urllib
import json

def init_app(app):
    players = ['João', 'Gustavo', 'Ana', 'Isabely']
    gamelist = [{'Título': 'CS 1.6', 'Ano': 1996, 'Categoria': 'FPS Online'}]
    
    
    # definindo a rota principal da aplicação '/'
    @app.route('/')
    # toda rota precisa de um função para executar 
    def home():
        return render_template('index.html')


    @app.route('/games', methods=['GET', 'POST'])
    def games():
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        # dicionário 
        console = {'Nome' : 'PS5', 'Fabricante': 'Sony', 'Ano': 2020}

        # tratando uma requisição POST com request
        if request.method == 'POST':
            # coletando o texto da input 
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))
        
        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)
    
    
    @app.route('/newGame', methods=['GET', 'POST'])
    def newGame():
        if request.method == 'POST':
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({'Título': request.form.get('title'), 'Ano': request.form.get('year'), 'Categoria' : request.form.get('category')})
                return redirect(url_for('newGame'))
                
        return render_template('newGame.html', gamelist=gamelist)
    
    
    @app.route('/apigames', methods=['GET', 'POST'])
    
    @app.route('/apigames/<id>', methods=['GET', 'POST'])
    def apigames(id=None): #Parametro opcional
        url = "https://www.freetogame.com/api/games"
        response = urllib.request.urlopen(url)
        data = response.read
        gamesList = json.loads(data)
        # Verificando se o parametro foi enviado
        if id:
            gameInfo = []
            for game in gamesList:
                if game['id'] == id: # Comparando os IDs
                    gameInfo = game
                    break
            if gameInfo:
                return render_template('gameinfo.html', gameInfo=gameInfo)
            else: 
                return f'Game com a ID {id} não foi encontrado'
        else:   
            return render_template('apigames.html', gamesList=gamesList)
    