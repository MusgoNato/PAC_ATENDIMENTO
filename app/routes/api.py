from flask import Blueprint, jsonify, g, request
from flask_login import login_required, current_user
from ..database.db import ServicoBancoDeDados
from ..routes.totem import ServicoTotem
import win32print
from datetime import datetime
from os import getenv
import string
import random
import time
import socket

SUCESSO = True
FALHA = False

api = Blueprint("api", __name__)

API_KEY_NODE_TO_FLASK = getenv("API_KEY_NODE_TO_FLASK")
PRINTER_NAME_IN_LOCAL_RASPBERRY = "ZDesigner GC420d"

# Configuracoes do IP, porta e tempo para conexao via socket com o raspberry local
PI_IP_RASPBERRY = getenv("PI_IP_RASPBERRY")
PI_PORT_RASPBERRY = int(getenv("PI_PORT_RASPBERRY"))
TIMEOUT_RASPBERRY = int(getenv("TIMEOUT_RASPBERRY"))

def gerar_senha_aleatoria(prefixo=None, tamanho=4):
    """Gera a senha aleatoria para o usuario final"""
    caracteres = string.ascii_letters + string.digits
    parte_random = ''.join(random.choices(caracteres,k=tamanho))

    if prefixo:
        return f"{prefixo.upper()}{parte_random}"
    else:
        return f"{parte_random}"

def generate_zebra_command(numero, tipo):
    """Funcao responsavel pela geracao do comando zpl para impressao na impressora ZEBRA DESIGNER GC420d"""
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # --- ZPL FINAL: Cortador Forçado e Comprimento Curto ---
    zpl_command = f"""^XA
    ^MNN           ; mídia contínua
    ^PW480         ; largura da etiqueta (≈ 60 mm)
    ^LL320         ; altura da etiqueta (≈ 40 mm)
    ^LH0,0

    ^FO0,80
    ^FB480,1,0,C,0
    ^A0N,70,70
    ^FD{numero}^FS

    ^FO0,170
    ^FB480,1,0,C,0
    ^A0N,60,60
    ^FD{tipo}^FS

    ^FO0,260
    ^FB480,1,0,C,0
    ^A0N,35,35
    ^FD{data}^FS

    ^XZ"""

    return zpl_command.strip()
        
# Nova função para validar a chave de API
def validate_api_key():
    """Verifica se o cabeçalho 'X-API-Key' está presente e é válido."""
    api_key = request.headers.get('X-API-Key')
    return api_key and api_key == API_KEY_NODE_TO_FLASK

@api.before_request
def before_request():
    """Cria uma nova conexao com o banco de dados para a requisicao atual."""
    try:
        g.db = ServicoBancoDeDados(*ServicoBancoDeDados._ServicoBancoDeDados__params)
        print("Conexao com o banco de dados aberta com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        g.db = None

@api.teardown_request
def teardown_request(exception=None):
    """Fecha a conexao com o banco de dados apos a requisicao."""
    db = g.pop("db", None)
    if db is not None:
        db.conn.close()
        print("Conexao com o banco de dados fechada com sucesso!")

#------------------Atendente------------------#

# Retorna a fila por completo
@api.route("/", methods=["GET"])
@login_required
def get_queue():
    """Responsavel pelo retorno dos dados da fila em espera"""
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados"}), 500
    try:
        cursor = g.db.cursor
        cursor.execute("SELECT id, numero, tipo FROM tickets WHERE status = 'AGUARDANDO' ORDER BY id ASC")
        filadb = cursor.fetchall()
        fila_formatada = []

        fila_formatada = [
            {'id': cliente['id'], 'numero': cliente['numero'], 'tipo': cliente['tipo']}
            for cliente in filadb
        ]

        return jsonify(fila_formatada)
    
    except Exception as e:
        print(f"Falha ao buscar a fila de espera : {e}")
        return jsonify({"error": "Falha ao buscar a fila de espera"})


@api.route("/chamar/<int:ticket_id>", methods=["POST"])
def chamar_cliente(ticket_id):
    """Função responsável por chamar um cliente para atendimento"""
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados"}), 500
    try:

        # Atualizacao das informacoes do ticket pelo corpo da requisição recebida pela API server.js
        cursor = g.db.cursor
        data = request.get_json()
        guiche_id = data.get("guiche_id")
        guiche_nome = data.get("guiche_nome")
        cursor.execute("UPDATE tickets SET status = 'CHAMADO', guiche_id = %s, guiche_nome = %s WHERE id = %s", (guiche_id, guiche_nome, ticket_id))
        g.db.conn.commit()

        return jsonify({"message" : f"ticket {ticket_id} chamado com sucesso."}), 200
    
    except Exception as e:
        print(f"Falha ao chamar cliente : {e}")
        g.db.conn.rollback()
        return jsonify({"error": "Falha ao chamar cliente"}), 500


# Rota para deletar o cliente
@api.route("/<int:ticket_id>", methods=["POST"])
def del_cliente(ticket_id):
    """Função responsável por deletar um cliente dentro da fila de espera"""
    if not validate_api_key():
        print("Chegou na funcao para delear cliente")
        return jsonify({"error": "Chave API key inválida."}), 401
    
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados"}), 500
    try:
        cursor = g.db.cursor
        cursor.execute("UPDATE tickets SET status = 'FINALIZADO' WHERE id = %s", ticket_id)
        g.db.conn.commit()

        return jsonify({"message" : f"ticket {ticket_id} finalizado com sucesso."}), 200
    
    except Exception as e:
        print(f"Falha ao deletar cliente : {e}")
        g.db.rollback()
        return jsonify({"error": "Falha ao deletar cliente"}), 500


@api.route("/em-atendimento", methods=["GET"])
@login_required
def get_cliente_em_atendimento():
    """Função responsável por retornar o cliente em atendimento de acordo com o guiche que fez essa requisição"""
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados!"}), 500
    try:
        # Retorna id do guiche, no caso o atendente
        guiche_id = current_user.id
        if not guiche_id:
            return jsonify({"error": "ID do guiche é necessario"}), 400
        
        cursor = g.db.cursor
        cursor.execute("SELECT id, numero, tipo FROM tickets WHERE status = 'CHAMADO' AND guiche_id = %s", (guiche_id))
        ticket = cursor.fetchone()

        if ticket:
            return jsonify({
                'id': ticket['id'],
                'numero': ticket['numero'],
                'tipo': ticket['tipo']
            }), 200
        else:
            return jsonify({"message" : f"Nenhum cliente em atendimento."}, 200)

    except Exception as e:
        print(f"Falha ao carregar cliente em atendimento : {e}")
        return jsonify({"error": "Falha ao carregar cliente em atendimento"}, 500)


# ----------------Totem---------------- #
@api.route("/nova_senha", methods=["POST"])
def gerar_senha():
    """Responsavel pelo PROCESSO de geração de senha"""
    if not validate_api_key():
        return jsonify({"error": "Chave de API inválida!"}), 401
    
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados"}, 500)
    data = request.get_json()
    tipo = data.get("category")

    # Primeiro cria a senha aleatoria
    senha_random = gerar_senha_aleatoria(prefixo=tipo)

    # Cria a senha no banco e depois devolve-a
    try:
        # Se chegou aqui, impressora está OK → gerar senha
        servico_totem = ServicoTotem(g.db)
        senha_gerada = servico_totem.set_nova_senha(tipo, senha_random)
        if senha_gerada == "Erro":
            raise Exception("Falha ao inserir senha no banco")
    except Exception as e:
        print(f"Erro ao gerar/salvar senha: {e}")
        return jsonify({"error": "Não foi possível gerar a senha no sistema."}), 500
    
    # 2. GERAÇÃO DO ZPL
    zpl_string = generate_zebra_command(senha_gerada, tipo)
    
    # 3. RETORNA DADOS PARA O NODE.JS
    return jsonify({
        "success": True,
        "ticket_number": senha_gerada,
        "category": tipo,
        "zpl_data": zpl_string,
    }), 200

#------------------Painel------------------#
@api.route("/painel", methods=["POST"])
def get_fila_para_atendimento():
    """Função responsável por retornar a fila para apresentação no painel"""
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados do painel!"}), 500
    
    if not validate_api_key():
        return jsonify({"error": "Não foi informado chave API na requisição para a fila de atendimento do painel!"}), 401
    try:

        cursor = g.db.cursor

        # Requisicao ao banco para retorno da fila, priorizando prioritários
        cursor.execute("""
        SELECT id, numero, tipo
                FROM tickets
                WHERE status = 'AGUARDANDO'
                ORDER BY
                    CASE
                        WHEN tipo = 'PRIORITARIO' THEN 1
                        ELSE 2
                    END,
                    id ASC
        """)

        # Retorna os dados da fila
        fila_db = cursor.fetchall()
        fila_formatada = [{'id': item['id'], 'numero': item['numero'], 'tipo': item['tipo']}
            for item in fila_db
        ]


        # Guiches em atendimento
        cursor.execute("SELECT id, numero, tipo, guiche_nome FROM tickets WHERE status = 'CHAMADO'")
        atendendo_db = cursor.fetchall()
        atendendo_formatado = [
            {'numero': item['numero'], 'tipo': item['tipo'], 'guiche_nome': item['guiche_nome']}
            for item in atendendo_db
        ]

        # Obtem os guiches disponiveis
        cursor.execute("SELECT id, nome FROM guiches WHERE ativo = 1")  
        guiches_db = cursor.fetchall()
        guiches_formatados = [
            {'id': item['id'], 'nome': item['nome']}
            for item in guiches_db
        ]

        # Construção da resposta
        response = {
            "fila_de_espera": fila_formatada,
            "guiches_atendimento": atendendo_formatado,
            "guiches_disponiveis": guiches_formatados
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": "Falha ao buscar a fila completa do painel de atendimento!"}), 500