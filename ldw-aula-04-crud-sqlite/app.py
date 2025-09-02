from flask import Flask, render_template
from controllers import routes
# Importando models
from models.database import db
# Importando a biblioteca para manipulação de S.O
import os 

# Criando uma instancia do Flask 
app = Flask(__name__, template_folder='views') # Esse parâmetro representa o nome da aplicação
routes.init_app(app)

# Extraindo diretorio absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))

#Criando o arquivo do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir,'models/games.sqlite3')

if __name__ == '__main__':
    db.init_app(app=app)
    # Verificar inicio da aplicação se o banco existe, se não, ele cria
    with app.test_request_context():
        db.create_all
    # Iniciando o servidor
    app.run(host="localhost", port=5000, debug=True) 

 