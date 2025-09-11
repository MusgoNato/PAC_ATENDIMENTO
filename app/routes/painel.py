from flask import Blueprint, render_template
from os import getenv

painel = Blueprint("painel", __name__)

# Home do Painel (Painel)
@painel.route("/")
def home():
    return render_template("painel/painel.html", API_URL_FLASK=getenv("API_URL_FLASK"), API_URL_NODE=getenv("API_URL_NODE"), URL_WEBSOCKET=getenv("URL_WEBSOCKET"))