from flask import Blueprint, render_template, jsonify, request

# Ao incluir o prefixo, nao e necessario especificar o nome da rota
totem = Blueprint("totem", __name__, url_prefix="/totem")

class ServicoTotem():
    def __init__(self):
        """
        Contrutor do servico Painel
        """
        pass

    def apresentacaoPainel(self):
        """
        Apresenta o painel para o usuario
        """
        pass

    def get_NovaSenha(self, tipo):
        """Funcao para gerar ticket"""
        match tipo:
            case "N":
                return "N"
            case "P":
                return "P"
            case _:
                return "DESCONHECIDO"



servico_totem = ServicoTotem()

# Home do usuario (Totem)
@totem.route("/")
def home():
    return render_template("/totem/totem.html")

@totem.route("/nova_senha", methods=["POST"])
def gerar_senha():
    data = request.get_json()
    tipo = data.get("category")
    senha_gerada = servico_totem.get_NovaSenha(tipo)
    return jsonify({"senha": senha_gerada})
