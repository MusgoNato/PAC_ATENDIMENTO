from flask import Blueprint, render_template, jsonify, request
from routes.totem import servico_totem

atendente = Blueprint("atendente", __name__, url_prefix="/atendente")
ultima_senha_chamada = None

@atendente.route("/")
def atendente_home():
    return render_template("atendente/atendente.html")

@atendente.route("/fila")
def fila_atual():
    fila = servico_totem.fila_prioritaria + servico_totem.fila_normal
    return jsonify({"fila": fila})

@atendente.route("/chamar_senha", methods=["POST"])
def chamar_senha_especifica():
    global ultima_senha_chamada
    data = request.get_json(silent=True) or {}
    senha = data.get("senha")

    if senha in servico_totem.fila_prioritaria:
        servico_totem.fila_prioritaria.remove(senha)
    elif senha in servico_totem.fila_normal:
        servico_totem.fila_normal.remove(senha)
    else:
        return jsonify({"erro": "Senha não encontrada"})

    ultima_senha_chamada = senha
    return jsonify({"chamada": senha})
