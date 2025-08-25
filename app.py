from flask import Flask
from .routes.totem import totem
from .routes.atendente import atendente
from .routes.painel import painel

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