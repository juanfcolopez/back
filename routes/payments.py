from itertools import count
from flask import jsonify, Blueprint
from db.data import db

payments_bp = Blueprint('routes-payments', __name__)

@payments_bp.route('/payments/count', methods=['GET'])
def types_count():
    pay_types = {}
    for receipt in db:
        for payment in receipt['payments']:
            if (payment['type'] not in pay_types): pay_types[payment['type']] = 1
            elif (payment['type'] in pay_types): pay_types[payment['type']] += 1
    method = []
    count = []
    for type in pay_types:
        method.append(type)
        count.append(pay_types[type])
    data = [method, count]
    return jsonify({ "data": data})

@payments_bp.route('/payments/amount', methods=['GET'])
def amount_by_method():
    pay_types = {}
    for receipt in db:
        for payment in receipt['payments']:
            if (payment['type'] not in pay_types): pay_types[payment['type']] = payment['amount']
            elif (payment['type'] in pay_types): pay_types[payment['type']] += payment['amount']
    data = []
    for method in pay_types:
        data.append({ 'Método': method, 'Cantidad ($)': pay_types[method] })
    return jsonify({ "data": data })


