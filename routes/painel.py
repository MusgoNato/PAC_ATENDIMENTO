from flask import Blueprint, render_template

painel = Blueprint("painel", __name__)

# Home do Painel (Painel)
@painel.route("/")
def home():
    return render_template("/painel/painel.html")