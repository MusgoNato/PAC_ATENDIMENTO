from flask import Flask
from routes.totem import totem
from routes.atendente import atendente
from routes.painel import painel
from database.db import ServicoBancoDeDados
from dotenv import load_dotenv
from os import getenv

<<<<<<< HEAD

# Carregamento das variáveis de ambiente
load_dotenv()
host, user, password, database = getenv("HOST"), getenv("USER"), getenv("PASSWORD"), getenv("DATABASE")


# Inicialização do banco de dados da aplicação
conn = ServicoBancoDeDados.getInstancia()
=======
# Carregamento das variaveis de ambiente
load_dotenv()
host, user, password, database = getenv("HOST"), getenv("USER"), getenv("PASSWORD"), getenv("DATABASE")

# Inicialização do banco de dados da aplicação
try:
    conn = ServicoBancoDeDados(host, user, password, database)
except Exception as e:
    raise Exception(f"Não foi possível inicializar a aplicação {e}")
>>>>>>> main


# Inicializa objeto da aplicação
app = Flask(__name__)


# Registro de blueprints
app.register_blueprint(painel)
app.register_blueprint(atendente)
app.register_blueprint(totem)


# Buscador para o app dentro do CPanel
application = app


# Execução local da aplicação
if __name__ == "__main__":
    app.run(debug=True)
