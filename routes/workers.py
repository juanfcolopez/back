from flask import jsonify, Blueprint, request
from db.data import db

workers_bp = Blueprint('routes-workers', __name__)

@workers_bp.route('/workers', methods=['GET'])
def workers_data():
    workers = {} 
    for receipt in db:
        if receipt['waiter'] not in workers:
            workers[receipt['waiter']] = {
                'Nombre': receipt['waiter'],
                'Cargo': 'Mesera/o'
                }
        if receipt['cashier'] not in workers:
            workers[receipt['cashier']] = {
                'Nombre': receipt['cashier'],
                'Cargo': 'Cajera/o'
                }
    data = [*workers.values()]
    return jsonify({ "data": data })

@workers_bp.route('/worker/tables/<name>', methods=['GET'])
def worker_freq_table_attention(name):
    table_attentions = {}
    for receipt in db:
        if receipt['cashier'] == name or receipt['waiter'] == name:
            if receipt['table'] not in table_attentions:
                table_attentions[receipt['table']] = {
                    'Mesa': receipt['table'],
                    'Dinero Total': receipt['total'],
                    'Atenciones': 1
                    }
            elif receipt['table'] in table_attentions:
                table_attentions[receipt['table']]['Dinero Total'] += receipt['total']
                table_attentions[receipt['table']]['Atenciones'] += 1
    data = [*table_attentions.values()]
    return jsonify({ "data": data })
