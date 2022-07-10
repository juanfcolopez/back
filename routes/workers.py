from flask import jsonify, Blueprint
from db.data import db
from aux.dates_validator import date_in_range, date_validator

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

@workers_bp.route('/worker/table/attention/<name>/<start>/<end>', methods=['GET'])
def tables_attention_by_date(name, start, end):
    table_attentions = {}
    if date_validator(start, end):
        for receipt in db:
            if name == receipt['cashier'] or name == receipt['waiter']:
                if date_in_range(start, end, receipt['date_closed']):            
                    if receipt['table'] not in table_attentions:
                        table_attentions[receipt['table']] = {
                            'Mesa': receipt['table'],
                            'Atenciones': 1,
                            'Total Recaudado': receipt['total']
                        }
                    elif receipt['table'] in table_attentions:
                        table_attentions[receipt['table']]['Atenciones'] += 1
                        table_attentions[receipt['table']]['Total Recaudado'] += receipt['total']
    data = [*table_attentions.values()]
    return jsonify({ "data": data })
