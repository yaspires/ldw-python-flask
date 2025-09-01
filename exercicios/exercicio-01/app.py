from flask import Flask, render_template
from controllers import routes

app = Flask(__name__, template_folder='views')

routes.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True) 

 