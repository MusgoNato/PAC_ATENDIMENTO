from flask import Blueprint, render_template

atendente = Blueprint("atendente", __name__)


class ServicoAtendente():
    def __init__(self):
        """
        Contrutor do servico do atendente
        """
        pass

    def atendimento_prox():
        """
        Proximo atendimento
        """
        pass

    def atendimento_ant():
        """
        Atendimento anterior
        """
        pass
    
    def move_cliente():
        """
        Move o cliente para outro guiche livre
        """


# Home do atendente (Painel do atendente)
@atendente.route("/atendente")
def home():
    return render_template("/atendente/atendente.html")

