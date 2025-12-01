from flask import Flask, request
from .routes.totem import totem
from .routes.atendente import atendente
from .routes.painel import painel
from .routes.api import api
from .database.db import ServicoBancoDeDados
from os import getenv
from flask_login import LoginManager
from .models.user import User
import os

# Carregamento das variaveis de ambiente
host, user, password, database, key_secret = getenv("DB_HOST"), getenv("DB_USER"), getenv("DB_PASSWORD"), getenv("DB_NAME"), getenv("KEY_SECRET")

# Inicialização do banco de dados da aplicação
try:
    ServicoBancoDeDados.setParametros(host, user, password, database)
except Exception as e:
    raise Exception(f"Não foi possível inicializar a aplicação {e}")


# Define o caminho para a pasta principal do projeto
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Inicializa objeto da aplicacao
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'), static_folder=os.path.join(basedir, 'static'))

# Configurar Flask-Login
app.secret_key = key_secret
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "atendente.login"

@login_manager.user_loader
def load_user(user_id):
    db_params = ServicoBancoDeDados._ServicoBancoDeDados__params
    if not db_params:
        # Parâmetros não definidos, não é possível conectar.
        return None 

    db = None
    try:
        db = ServicoBancoDeDados(*db_params)
        cursor = db.cursor
        cursor.execute("SELECT * FROM guiches WHERE id=%s", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return User(id=row['id'], username=row['nome'])
        return None
    except Exception as e:
        print(f"Erro ao carregar usuário: {e}")
        return None
    finally:
        if db is not None:
            db.conn.close()


# Registrar os blueprints
app.register_blueprint(painel)
app.register_blueprint(atendente, url_prefix='/atendente')
app.register_blueprint(totem, url_prefix='/totem')
app.register_blueprint(api, url_prefix='/api/v1/fila')


# Buscador para o app dentro do CPanel
application = app