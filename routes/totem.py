from flask import Blueprint, render_template, jsonify, request
import random

# Ao incluir o prefixo, nao e necessario especificar o nome da rota
totem = Blueprint("totem", __name__, url_prefix="/totem")

class ServicoTotem():
    def __init__(self):
        """
        Contrutor do servico Painel
        """
        self.resultados = {
            "P": set(),
            "N": set(),
        }

    def apresentacaoPainel(self):
        """
        Apresenta o painel para o usuario
        """
        pass

    def get_NovaSenha(self, tipo: str) -> str:
        """Funcao para gerar ticket"""
        tipo = (tipo or "").upper()

        match tipo:
            case "N":
                return "N"
            case "P":
                while True:
                    senhaP = random.randint(1, 999)
                    if senhaP not in self.resultados["P"]:
                        self.resultados["P"].add(senhaP)
                        return f"P{senhaP:03}"
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
