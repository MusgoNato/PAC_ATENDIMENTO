from flask import Blueprint, render_template, jsonify, request
from database.db import ServicoBancoDeDados

# Ao incluir o prefixo, nao e necessario especificar o nome da rota
totem = Blueprint("totem", __name__, url_prefix="/totem")

class ServicoTotem():
    def __init__(self):
        """
        Conexao com o banco de dados (Single Ton)
        """
        self.db = ServicoBancoDeDados.getInstancia()

    def get_NovaSenha(self, tipo):
        cursor = self.db.cursor
        match tipo:
            case "N":
                tipo_db = 'NORMAL'
            case "P":
                tipo_db = 'PRIORITARIO'
            case _:
                return "Erro: Tipo de ticket invalido"
        try:
            # Insere a nova senha no banco de dados.
            cursor.execute(
                "INSERT INTO tickets (tipo) VALUES (%s)",
                (tipo_db,)
            )
            
            # Pega o ID gerado pela inserção.
            novo_id = cursor.lastrowid

            # Confirma a transação.
            self.db.conn.commit()
            
            # Formata a senha com base no tipo e no ID.
            nova_senha_formatada = f"{tipo}{novo_id:03d}"
            
            # 4. Atualiza o registro com a senha formatada.
            cursor.execute(
                "UPDATE tickets SET numero = %s WHERE id = %s",
                (nova_senha_formatada, novo_id)
            )
            self.db.conn.commit()
            
            return nova_senha_formatada

        except Exception as e:
            # Em caso de erro, desfaz a operação e loga o erro.
            self.db.conn.rollback()
            print(f"Erro ao inserir senha: {e}")
            return "Erro"

# Home do usuario (Totem)
@totem.route("/")
def home():
    return render_template("/totem/totem.html")

@totem.route("/nova_senha", methods=["POST"])
def gerar_senha():
    data = request.get_json()
    tipo = data.get("category")
    servico_totem = ServicoTotem()
    senha_gerada = servico_totem.get_NovaSenha(tipo)

    # Conexao com a impressora para sair a senha
    #### ---- ####

    return jsonify({"senha": senha_gerada})