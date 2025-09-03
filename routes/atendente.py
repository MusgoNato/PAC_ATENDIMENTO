from flask import request, redirect, url_for, render_template, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from models.user import User
from database.db import ServicoBancoDeDados

atendente = Blueprint("atendente", __name__, url_prefix="/atendente")

class ServicoAtendente():
    def __init__(self):
        """
        Contrutor do servico do atendente
        """
        self.db = ServicoBancoDeDados.getInstancia()

# Home do atendente (Painel do atendente)
@atendente.route("/login", methods=["GET", "POST"])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for("atendente.home"))
    
    if request.method == "POST":

        nome = request.form.get("username")
        senha = request.form.get("password")
        
        # Login no banco de dados
        servico_atendente = ServicoAtendente()

        cursor = servico_atendente.db.cursor
        
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

@atendente.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("atendente.login"))

# Pagina do atendente apos logado
@atendente.route("/home", methods=["GET"])
@login_required
def home():
    nome_guiche = session.get('nome_guiche', 'Guichê Padrão')
    return render_template("atendente/home.html", nome_guiche=nome_guiche)