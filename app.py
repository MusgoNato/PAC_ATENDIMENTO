from os import getenv
from dotenv import load_dotenv
from flask import Flask
from routes.totem import totem
from routes.atendente import atendente
from routes.painel import painel
from database.db import ServicoBancoDeDados

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as credenciais do banco
host = getenv("HOST")
user = getenv("USER")
password = getenv("PASSWORD")
database = getenv("DATABASE")

# Inicializa conexão com o banco de dados
try:
    conn = ServicoBancoDeDados(host, user, password, database)
except Exception as e:
    raise RuntimeError(f"Não foi possível inicializar a aplicação: {e}")

# Cria a aplicação Flask
app = Flask(__name__, template_folder="templates")

# Registro dos módulos (blueprints)
app.register_blueprint(painel)
app.register_blueprint(atendente)
app.register_blueprint(totem)

# Compatibilidade com CPanel (espera 'application' como entrypoint)
application = app

# Execução local
if __name__ == "__main__":
    app.run(
        debug=True,        # Debug ativo apenas no ambiente local
        host="0.0.0.0",    # Permite acesso externo na rede local
        port=5000
    )
