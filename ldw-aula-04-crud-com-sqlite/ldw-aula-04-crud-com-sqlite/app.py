# Importando o Flask
from flask import Flask, render_template
# Importando o Controller (routes.py)
from controllers import routes
# Importando os Models
from models.database import db
# Importando a biblioteca para manipulação do S.O
import os

# Criando uma instância do Flask
app = Flask(__name__, template_folder='views')  # __name__ representa o nome da aplicação
routes.init_app(app)

# Extraindo o diretório absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))
# Criando o arquivo do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')
# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    # Enviando o Flask para SqlAlchemy
    db.init_app(app=app)
    # Verificar no início da aplicação se o BD já existe. Se não, ele cria.
    with app.test_request_context():
        db.create_all()          
    # Iniciando o servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
