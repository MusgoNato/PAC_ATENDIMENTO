from flask import Blueprint, render_template, jsonify, request

totem = Blueprint("totem", __name__, url_prefix="/totem")

class ServicoTotem:
    def __init__(self):
        """Construtor do serviço Totem. Mantém filas separadas e contadores sequenciais."""
        self.contador_normal = 0
        self.contador_prioritario = 0
        self.fila_normal = []
        self.fila_prioritaria = []

    def get_NovaSenha(self, tipo: str) -> str:
        """Gera uma nova senha sequencial. Tipo: 'P' = Prioritária, 'N' = Normal."""
        tipo = tipo.upper()
        if tipo not in ("P", "N"):
            return "TIPO_INVÁLIDO"

        if tipo == "N":
            self.contador_normal += 1
            numero = self.contador_normal
            senha = f"N{numero:03d}"
            self.fila_normal.append(senha)
        else:
            self.contador_prioritario += 1
            numero = self.contador_prioritario
            senha = f"P{numero:03d}"
            self.fila_prioritaria.append(senha)

        return senha

    def chamar_proxima(self):
        """Chama a próxima senha, priorizando a fila prioritária."""
        if self.fila_prioritaria:
            return self.fila_prioritaria.pop(0)
        elif self.fila_normal:
            return self.fila_normal.pop(0)
        return None

# Instância do serviço
servico_totem = ServicoTotem()

# Home do usuário (Totem)
@totem.route("/")
def home():
    return render_template("/totem/totem.html")

@totem.route("/nova_senha", methods=["POST"])
def gerar_senha():
    """Endpoint para gerar uma nova senha."""
    data = request.get_json(silent=True) or {}
    tipo = data.get("category", "").upper()  # Espera "N" ou "P"
    senha_gerada = servico_totem.get_NovaSenha(tipo)
    return jsonify({"senha": senha_gerada})

@totem.route("/chamar", methods=["GET"])
def chamar_senha():
    """Endpoint para chamar a próxima senha."""
    senha = servico_totem.chamar_proxima()
    if senha:
        return jsonify({"proxima": senha})
    return jsonify({"mensagem": "Nenhuma senha na fila"})
