from flask import Blueprint, jsonify, g, request
from flask_login import login_required, current_user
from ..database.db import ServicoBancoDeDados
from ..routes.totem import ServicoTotem
import win32print
import win32con
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from os import getenv

SUCESSO = True
FALHA = False

api = Blueprint("api", __name__)

API_KEY_NODE_TO_FLASK = getenv("API_KEY_NODE_TO_FLASK")
PRINTER_NAME = "TSC DA200O"

# Reponsavel por verificar se a impressora esta on/off
def impressora_online():
    try:
        hprinter = win32print.OpenPrinter(PRINTER_NAME)
        printer_info = win32print.GetPrinter(hprinter, 2)
        win32print.ClosePrinter(hprinter)

        status = printer_info["Status"]
        attributes = printer_info["Attributes"]

        if status & win32print.PRINTER_STATUS_OFFLINE or attributes & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE:
            return False
        return True
    except:
        return False

def image_to_tspl(img, x=20, y=20):
    """
    Converte imagem PIL (1-bit) para comando TSPL BITMAP
    """
    width, height = img.size
    width_bytes = (width + 7) // 8  # cada byte = 8 pixels

    # Converte pixels em bytes
    pixels = img.load()
    data = bytearray()
    for row in range(height):
        for byte_idx in range(width_bytes):
            byte = 0
            for bit in range(8):
                col = byte_idx * 8 + bit
                if col < width:
                    pixel = pixels[col, row]
                    if pixel == 0:  # preto
                        byte |= (1 << (7 - bit))
            data.append(byte)

    # Comando TSPL: BITMAP x,y,width_bytes,height,mode,data
    # mode=0 (OR), mode=1 (XOR), normalmente 0
    header = f"BITMAP {x},{y},{width_bytes},{height},0,".encode("utf-8")
    return header + data + b"\n"

def text_to_bitmap(text, font_size=24, padding=10):
    # Fonte padrão do PIL
    font = ImageFont.load_default()

    # Cria imagem temporária só para medir o texto
    dummy_img = Image.new("1", (1, 1), "white")
    draw = ImageDraw.Draw(dummy_img)

    # Mede o tamanho do texto corretamente
    try:
        # Pillow mais novo → usa textbbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        # Pillow mais antigo → usa textsize
        text_w, text_h = draw.textsize(text, font=font)

    # Cria imagem final em branco (fundo branco, texto preto)
    img = Image.new("1", (text_w + padding * 2, text_h + padding * 2), 1)  # 1-bit, branco
    draw = ImageDraw.Draw(img)
    draw.text((padding, padding), text, font=font, fill=0)  # fill=0 → preto

    return img

# Responsavel pelo envio do ticket a ser impresso
def print_knup(numero, tipo):
    hprinter = None
    try:
        hprinter = win32print.OpenPrinter(PRINTER_NAME)
        printer_info = win32print.GetPrinter(hprinter, 2)

        # Checa status da impressora
        status = printer_info["Status"]
        attributes = printer_info["Attributes"]

        # Flags comuns de problema
        if status & win32print.PRINTER_STATUS_OFFLINE or attributes & win32print.PRINTER_ATTRIBUTE_WORK_OFFLINE:
            print("Impressora está offline/desplugada!")
            return FALHA

        # Se chegou aqui, impressora está online → envia comando
        doc_info = ("TSPL Job", None, "RAW")
        hjob = win32print.StartDocPrinter(hprinter, 1, doc_info)
        win32print.StartPagePrinter(hprinter)

        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        img = text_to_bitmap(f"SENHA: {numero}\nTIPO: {tipo}\n{data}", font_size=120)

        # Converte para 1-bit a imagem resultante
        img = img.convert('1')

        # Dobra o tamanho da imagem inteira
        img = img.resize((img.width * 6, img.height * 6))

        # Converte para TSPL
        tspl_header = b"SIZE 60 mm,40 mm\nCLS\n"
        tspl_img = image_to_tspl(img, 20, 20)
        tspl_footer = b"PRINT 1\n"

        win32print.WritePrinter(hprinter, tspl_header + tspl_img + tspl_footer)
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
        return SUCESSO

    except Exception as e:
        print(f"Erro ao imprimir/conectar impressora KNUP: {e}")
        return FALHA
    finally:
        if hprinter is not None:
            try:
                win32print.ClosePrinter(hprinter)
            except:
                pass

# Nova função para validar a chave de API
def validate_api_key():
    """Verifica se o cabeçalho 'X-API-Key' está presente e é válido."""
    api_key = request.headers.get('X-API-Key')
    return api_key and api_key == API_KEY_NODE_TO_FLASK

# Este hook e executado ANTES de cada requisicao
@api.before_request
def before_request():
    """Cria uma nova conexao com o banco de dados para a requisicao atual."""
    try:
        g.db = ServicoBancoDeDados(*ServicoBancoDeDados._ServicoBancoDeDados__params)
        print("Conexao com o banco de dados aberta com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        g.db = None

# Este hook e executado DEPOIS de cada requisicao
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
    if not validate_api_key():
        return jsonify({"error": "Chave de API inválida!"}), 401
    
    if g.db is None:
        return jsonify({"error": "Falha na conexao com o banco de dados"}, 500)
    data = request.get_json()
    tipo = data.get("category")

    # Primeiro: checar se impressora está online
    if not impressora_online():
        print("Impressora offline, senha não será gerada")
        return jsonify({
            "status": "erro_impressao",
            "mensagem": "A impressora está offline. Aguarde o suporte!"
        }), 200

    try:
        # Se chegou aqui, impressora está OK → gerar senha
        servico_totem = ServicoTotem(g.db)
        senha_gerada = servico_totem.get_NovaSenha(tipo)
    except Exception as e:
        print(f"Erro ao gerar/salvar senha: {e}")
        return jsonify({"error": "Não foi possível gerar a senha no sistema."}), 500

    # Agora tenta imprimir de fato
    if not print_knup(senha_gerada, tipo):
        return jsonify({
            "senha": senha_gerada,
            "status": "erro_impressao",
            "mensagem": "Falha na impressao, mas senha gerada normalmente, provavelmente no momento que envio a impressao deu falha ou desplugou a impressora termica"
        }), 200
    else:
        # Senha gerada e impressa
        return jsonify({
            "senha": senha_gerada,
            "status": "impresso"
        }), 200


#------------------Painel------------------#
@api.route("/painel", methods=["POST"])
def get_fila_para_atendimento():
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