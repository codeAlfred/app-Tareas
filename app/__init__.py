from flask import Flask

from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
bootstrap= Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()

from .views import page
from .models import User, Task

def create_app(config):
    # apartir del objeto config el servidor se configurara
    app.config.from_object(config)

    # iniciamos el csrf en nuestra app
    csrf.init_app(app)
    login_manager.init_app(app)
    # redireccionando al login cuando no estas autenticado y quieres entrar a las Tareas
    login_manager.login_view = '.login'
    login_manager.login_message = 'Es necesario iniciar sesion'


    # asignacion bootstrap
    bootstrap.init_app(app)
    # registrar page en app
    app.register_blueprint(page)

    # creamos un contexto
    with app.app_context():
        # iniciamos la bd a partir del sevidor
        db.init_app(app)
        db.create_all()

    return app