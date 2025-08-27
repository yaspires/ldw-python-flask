from flask import Flask, render_template
from controllers import routes

# Criando uma instancia do Flask 
app = Flask(__name__, template_folder='views') # Esse parâmetro representa o nome da aplicação

routes.init_app(app)

if __name__ == '__main__':
    # Iniciando o servidor
    app.run(host="localhost", port=5000, debug=True) 

 