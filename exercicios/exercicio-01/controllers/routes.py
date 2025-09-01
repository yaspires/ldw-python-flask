from flask import render_template, request, redirect, url_for

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
    