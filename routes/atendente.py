from flask import Blueprint, render_template

atendente = Blueprint("atendente", __name__)

# Home do atendente (Painel do atendente)
@atendente.route("/atendente")
def home():
    return render_template("/atendente/atendente.html")