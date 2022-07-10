from flask import jsonify, Blueprint
from db.data import db
from aux.dates_validator import date_in_range, date_validator

payments_bp = Blueprint('routes-payments', __name__)

@payments_bp.route('/payments/count/<start>/<end>', methods=['GET'])
def types_count_cash_and_freq(start, end):
    pay_types = {}
    if date_validator(start, end):
        for receipt in db:
            if date_in_range(start, end, receipt['date_closed']):
                for payment in receipt['payments']:
                    if (payment['type'] not in pay_types):
                        pay_types[payment['type']] = {'count': 1, 'amount': payment['amount']}

                    elif (payment['type'] in pay_types):
                        pay_types[payment['type']]['count'] += 1
                        pay_types[payment['type']]['amount'] += payment['amount']
        method = []
        count = []
        cash_amount_by_payment = []
        for type in pay_types:
            method.append(type)
            count.append(pay_types[type]['count'])
            cash_amount_by_payment.append({'Método': type, 'Cantidad ($)': pay_types[type]['amount']})
    data = [method, count, cash_amount_by_payment]
    return jsonify({ "data": data})
