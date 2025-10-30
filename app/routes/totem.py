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
        Conexao com o banco de dados (Single Ton)
        """
        self.db = db_connection

    def set_nova_senha(self, tipo, senha_gerada):
        """Função responsável por setar uma nova senha"""
        cursor = self.db.cursor

        try:
            cursor.execute(
                "INSERT INTO tickets (tipo, numero) VALUES (%s, %s)",
                (tipo, senha_gerada)
            )

            self.db.conn.commit()

            # Retorna a senha gerada, agora cadastrada no banco
            return senha_gerada

        except Exception as e:
            # Em caso de erro, desfaz a operação e loga o erro.
            self.db.conn.rollback()
            print(f"Erro ao inserir senha: {e}")
            return "Erro"


# Home do usuario (Totem)
@totem.route("")
def home():
    # Passando as variaveis de ambiente de forma dinamica 
    return render_template("totem/totem.html", API_URL_FLASK=getenv("API_URL_FLASK"), API_URL_NODE=getenv("API_URL_NODE"))