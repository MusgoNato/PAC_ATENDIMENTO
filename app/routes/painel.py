from flask import Blueprint, render_template

painel = Blueprint("painel", __name__)

class ServicoPainel():
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

# Home do Painel (Painel)
@painel.route("/")
def home():
    return render_template("/painel/painel.html")