from flask import Blueprint, jsonify, session
from flask_login import login_required, current_user
from ..database.db import ServicoBancoDeDados

api = Blueprint("api", __name__)

# Retorna a fila por completo
@api.route("/api/v1/fila", methods=["GET"])
@login_required
def get_queue():
    try:
        db = ServicoBancoDeDados.getInstancia()
        cursor = db.cursor
        cursor.execute("SELECT id, numero, tipo FROM tickets WHERE status = 'AGUARDANDO' ORDER BY id ASC")
        filadb = cursor.fetchall()
        fila_formatada = []

        for cliente in filadb:
            fila_formatada.append({
                'id': cliente['id'],
                'numero': cliente['numero'],
                'tipo': cliente['tipo']
            })

        return jsonify(fila_formatada)
    
    except Exception as e:
        print(f"Falha ao buscar a fila de espera : {e}")
        return jsonify({"error": "Falha ao buscar a fila de espera"})


@api.route("/api/v1/fila/chamar/<int:ticket_id>", methods=["POST"])
@login_required
def chamar_cliente(ticket_id):
    try:
        db = ServicoBancoDeDados.getInstancia()
        cursor = db.cursor
        guiche_id = current_user.id
        guiche_nome = session.get("nome_guiche", "NULL")
        cursor.execute("UPDATE tickets SET status = 'CHAMADO', guiche_id = %s, guiche_nome = %s WHERE id = %s", (guiche_id, guiche_nome, ticket_id))
        db.conn.commit()

        return jsonify({"message" : f"ticket {ticket_id} chamado com sucesso."}, 200)
    
    except Exception as e:
        print(f"Falha ao chamar cliente : {e}")
        return jsonify({"error": "Falha ao chamar cliente"}, 500)


# Rota para deletar o cliente
@api.route("/api/v1/fila/<int:ticket_id>", methods=["DELETE"])
@login_required
def del_cliente(ticket_id):
    try:
        db = ServicoBancoDeDados.getInstancia()
        cursor = db.cursor
        cursor.execute("UPDATE tickets SET status = 'FINALIZADO' WHERE id = %s", ticket_id)
        db.conn.commit()

        return jsonify({"message" : f"ticket {ticket_id} finalizado com sucesso."}, 200)
    
    except Exception as e:
        print(f"Falha ao deletar cliente : {e}")
        return jsonify({"error": "Falha ao deletar cliente"}, 500)


@api.route("/api/v1/fila/em-atendimento", methods=["GET"])
@login_required
def get_cliente_em_atendimento():
    try:
        db = ServicoBancoDeDados.getInstancia()
        cursor = db.cursor
        cursor.execute("SELECT id, numero, tipo FROM tickets WHERE status = 'CHAMADO' AND guiche_id = %s", (current_user.id))
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
