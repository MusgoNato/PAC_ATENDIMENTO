from flask import request, redirect, url_for, render_template, Blueprint, session, g, jsonify
from flask_login import login_user, login_required, logout_user
from ..models.user import User
from ..database.db import ServicoBancoDeDados
from os import getenv

atendente = Blueprint("atendente", __name__, url_prefix="/atendente")


@atendente.before_request
def before_request():
    """Cria uma nova conexao com o banco de dados para a requisição atual"""
    try:
        g.db = ServicoBancoDeDados(*ServicoBancoDeDados._ServicoBancoDeDados__params)
        print("Conexao com o banco de dados aberta com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados {e}")
        g.db = None

@atendente.teardown_request
def teardown_request(exception=None):
    """Fecha a requisição com o banco de dados após a requisição"""
    db = g.pop("db", None)
    if db is not None:
        db.conn.close()
        print("Conexao com o banco de dados fechada com sucesso.")

# Home do atendente (Painel do atendente)
@atendente.route("/login", methods=["GET", "POST"])
def login():    
    if request.method == "POST":
        if g.db is None:
            return jsonify({"error": "Erro ao conectar com o banco de dados!"}), 500
        
        nome = request.form.get("username")
        senha = request.form.get("password")
        
        # Login no banco de dados
        cursor = g.db.cursor
        
        cursor.execute(
            "SELECT * FROM guiches WHERE nome=%s AND password=%s",
            (nome, senha)
        )
        usuario = cursor.fetchone()

        # Caso o usuario esteja autenticado, salvo na sessao do navegador e redireciono a url
        if usuario:
            user = User(id=usuario['id'], username=usuario['nome'])
            login_user(user)
            session['nome_guiche'] = usuario['nome']
            return redirect(url_for("atendente.home"))
        else:
            return render_template("atendente/login.html", error="Usuário ou senha incorretos")

    # Qualquer tipo que difere de POST cai na renderização da propria pagina novamente
    return render_template("atendente/login.html")

# Pagina do atendente apos logado
@atendente.route("/home", methods=["GET"])
@login_required
def home():
    nome_guiche = session.get('nome_guiche', 'Guichê Padrão')
    return render_template("atendente/home.html", nome_guiche=nome_guiche, API_URL_FLASK=getenv("API_URL_FLASK"), API_URL_NODE=getenv("API_URL_NODE"), URL_WEBSOCKET=getenv("URL_WEBSOCKET"))

@atendente.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('atendente.login'))

# COLE ESTE CÓDIGO NO FINAL DO SEU ARQUIVO atendente.py

@atendente.route("/chamar/<int:ticket_id>", methods=["POST"])
@login_required
def chamar_senha(ticket_id):
    # Pega os dados do guichê (enviados pelo Node.js a partir do frontend)
    dados_guiche = request.get_json()
    guiche_id = dados_guiche.get('guiche_id')
    guiche_nome = dados_guiche.get('guiche_nome')

    # Validação para garantir que o nome do guichê foi enviado
    if not guiche_nome:
        return jsonify({"success": False, "error": "Nome do guichê não fornecido"}), 400

    # Verifica se a conexão com o banco de dados existe
    if g.db is None:
        return jsonify({"success": False, "error": "Erro de conexão com o banco de dados"}), 500

    cursor = g.db.cursor
    
    try:
        # --- LÓGICA PRINCIPAL DA CORREÇÃO ---

        # PASSO 1: REMOVER O ATENDIMENTO ANTERIOR DESTE GUICHÊ
        # Isso garante que senhas antigas não fiquem presas no painel.
        # (Assumindo que sua tabela se chama 'atendimentos_ativos'. Se for outro nome, ajuste aqui.)
        cursor.execute(
            "DELETE FROM data.guiches_atendimento WHERE guiche_nome = %s",
            (guiche_nome,)
        )

        # PASSO 2: BUSCAR OS DADOS DA SENHA QUE SERÁ ATENDIDA
        # Apenas busca senhas que ainda estão aguardando.
        cursor.execute(
            "SELECT numero, tipo FROM tickets WHERE id = %s AND status = 'AGUARDANDO'",
            (ticket_id,)
        )
        ticket = cursor.fetchone()

        # Se a senha não for encontrada (talvez outro guichê já a chamou), retorna um erro.
        if not ticket:
            g.db.conn.rollback() # Desfaz o DELETE do Passo 1
            return jsonify({"success": False, "error": "Ticket não encontrado ou já em atendimento"}), 404

        # Atualiza o status da senha para que não seja chamada novamente.
        cursor.execute(
            "UPDATE tickets SET status = 'EM ATENDIMENTO' WHERE id = %s",
            (ticket_id,)
        )

        # PASSO 3: ADICIONAR O NOVO REGISTRO DE ATENDIMENTO
        # Insere a nova senha que este guichê está atendendo agora.
        cursor.execute(
            "INSERT INTO atendimentos_ativos (guiche_id, guiche_nome, ticket_id, numero_senha, tipo_senha) VALUES (%s, %s, %s, %s, %s)",
            (guiche_id, guiche_nome, ticket_id, ticket['numero'], ticket['tipo'])
        )
        
        # Confirma todas as operações (DELETE, UPDATE, INSERT) no banco de dados.
        g.db.conn.commit()

        # Retorna uma mensagem de sucesso para o Node.js/frontend.
        return jsonify({
            "success": True,
            "message": f"Senha {ticket['numero']} chamada com sucesso no guichê {guiche_nome}"
        })

    except Exception as e:
        # Se qualquer passo falhar, desfaz todas as operações para manter o banco consistente.
        g.db.conn.rollback()
        print(f"ERRO CRÍTICO ao chamar senha: {e}")
        return jsonify({"success": False, "error": "Ocorreu um erro interno ao processar a chamada"}), 500