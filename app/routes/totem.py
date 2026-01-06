from flask import Blueprint, render_template, g
from ..database.db import ServicoBancoDeDados
from os import getenv

# Ao incluir o prefixo, nao e necessario especificar o nome da rota
totem = Blueprint("totem", __name__, url_prefix="/totem")

@totem.before_request
def before_request():
    """Cria uma nova conexao com o banco de dados para a requisição atual"""
    try:
        g.db = ServicoBancoDeDados(*ServicoBancoDeDados._ServicoBancoDeDados__params)
        print("Conexao com o banco de dados aberta com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {e}")
        g.db = None

@totem.teardown_request
def teardown_request(exception=None):
    """Fecha a requisição com o banco de dados após a requisição"""
    db = g.pop("db", None)
    if db is not None:
        db.conn.close()
        print("Conexao com o banco de dados fechada com sucesso.")

class ServicoTotem():
    def __init__(self, db_connection):
        """
        Conexao com o banco de dados
        """
        self.db = db_connection

    def get_nova_senha(self, tipo):
        """Função responsável por setar uma nova senha"""
        cursor = self.db.cursor
        if tipo == "P":
            qual_tipo = "PRIORITARIO"
        elif tipo == "N":
            qual_tipo = "NORMAL"


        try:
            cursor.execute(
                "INSERT INTO tickets (tipo) VALUES (%s)",
                (qual_tipo)
            )

            novo_id = cursor.lastrowid

            self.db.conn.commit()

            nova_senha_formatada = f"{tipo}{novo_id:03d}"

            cursor.execute(
                "UPDATE tickets SET numero = %s WHERE id = %s",
                (nova_senha_formatada, novo_id)
            )

            self.db.conn.commit()

            # Retorna a senha gerada, agora cadastrada no banco
            return nova_senha_formatada

        except Exception as e:
            # Em caso de erro, desfaz a operação e loga o erro.
            self.db.conn.rollback()
            print(f"Erro ao inserir senha: {e}", flush=True)
            return "ErroBD"


# Home do usuario (Totem)
@totem.route("")
def home():
    # Passando as variaveis de ambiente de forma dinamica 
    return render_template("totem/totem.html", API_URL_FLASK=getenv("API_URL_FLASK"), API_URL_NODE=getenv("API_URL_NODE"))