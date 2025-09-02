from flask import request, redirect, url_for, render_template, Blueprint, session, g, jsonify
from flask_login import login_user, login_required, logout_user
from ..models.user import User
from ..database.db import ServicoBancoDeDados

atendente = Blueprint("atendente", __name__)


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
    return render_template("atendente/home.html", nome_guiche=nome_guiche)

@atendente.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('atendente.login'))