from flask import Flask
from .routes.totem import totem
from .routes.atendente import atendente
from .routes.painel import painel
from .database.db import ServicoBancoDeDados
from dotenv import load_dotenv
from os import getenv

# Carregamento das variaveis de ambiente
# load_dotenv()
# host, user, password, database = getenv("HOST"), getenv("USER"), getenv("PASSWORD"), getenv("DATABASE")

# Inicialização do banco de dados da aplicação
# conn = ServicoBancoDeDados.getInstancia()

# Inicializa objeto da aplicacao
app = Flask(__name__)

# Registro de blueprints

# Painel
app.register_blueprint(painel)

# Atendente
app.register_blueprint(atendente)

# Totem do usuario
app.register_blueprint(totem)

# Buscador para o app dentro do CPanel
application = app