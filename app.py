from flask import Flask
from flask_socketio import SocketIO
from routes.totem import totem
from routes.atendente import atendente
from routes.painel import painel
from routes.api import api
from database.db import ServicoBancoDeDados
from dotenv import load_dotenv
from os import getenv
from flask_login import LoginManager
from models.user import User

# Carregamento das variaveis de ambiente
load_dotenv()
host, user, password, database, key_secret = getenv("HOST"), getenv("DB_USER"), getenv("PASSWORD"), getenv("DATABASE"), getenv("KEY_SECRET")

print(host, user, password, database, key_secret)

# Inicialização do banco de dados da aplicação
try:
    ServicoBancoDeDados.setParametros(host, user, password, database)
except Exception as e:
    raise Exception(f"Não foi possível inicializar a aplicação {e}")

# Inicializa objeto da aplicacao
app = Flask(__name__)

# Configurar Flask-Login
app.secret_key = key_secret
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "atendente.login"


@login_manager.user_loader
def load_user(user_id):
    db = ServicoBancoDeDados.getInstancia()
    cursor = db.cursor
    cursor.execute("SELECT * FROM guiches WHERE id=%s", (user_id,))
    row = cursor.fetchone()
    if row:
        return User(id=row['id'], username=row['nome'])
    return None

# Registro de blueprints

# Painel
app.register_blueprint(painel)

# Atendente
app.register_blueprint(atendente)

# Totem do usuario
app.register_blueprint(totem)

# API
app.register_blueprint(api)

# Buscador para o app dentro do CPanel
application = app