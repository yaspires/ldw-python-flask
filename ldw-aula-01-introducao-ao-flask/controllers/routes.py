from flask import render_template

def init_app(app):
    # Definindo a rota principal da aplicação '/'
    @app.route('/') 
    def home():
        return render_template('index.html')


    @app.route('/games')
    def games():
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        # lista 
        players = ['João', 'Gustavo', 'Ana', 'Isabely']
        # dicionário 
        console = {'Nome' : 'PS5', 'Fabricante': 'Sony', 'Ano': 2020}
        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)