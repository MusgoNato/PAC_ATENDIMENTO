from flask import Blueprint, render_template

totem = Blueprint("totem", __name__)

class ServicoTotem():
    def __init__(self):
        """
        Contrutor do servico Painel
        """
        pass

    def apresentacaoPainel():
        """
        Apresenta o painel para o usuario
        """
        pass

# Home do usuario (Totem)
@totem.route("/totem")
def home():
    return render_template("/totem/totem.html")