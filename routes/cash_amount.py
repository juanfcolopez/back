from flask import jsonify, Blueprint, request
from db.data import db
from aux.dates_validator import end_date_formatter, start_date_formatter, date_formatter
import datetime
cash_amount_bp = Blueprint('routes-cash_amount', __name__)

@cash_amount_bp.route('/amount/<start>/<end>', methods=['GET'])
def amount_by_date(start, end):
    date_data = {}
    data = []
    start = start_date_formatter(start)
    end = end_date_formatter(end)
    days = []
    if (start < end):
      delta = end - start
      days = [(start + datetime.timedelta(days=x)).strftime('%d-%m-%Y') for x in range(0, delta.days+1)]
    for day in days:
        date_data[day] = {'Total diario': 0}
    for receipt in db:
        current_date = date_formatter(receipt['date_closed'])
        if start <= current_date <= end:
            date_data[current_date.strftime('%d-%m-%Y')]['Total diario'] += receipt['total']
    amount = []
    for day in days:
        amount.append(date_data[day]['Total diario'])
    data = [days, amount]
    return jsonify({ "data": data })

@cash_amount_bp.route('/amount/years', methods=['GET'])
def years_with_data():
    data = []
    for receipt in db:
        current_date = datetime.datetime.strptime(receipt['date_closed'], "%Y-%m-%d %H:%M:%S")
        year = current_date.strftime('%Y')
        if year not in data: data.append(year)
    return jsonify({ "data": data })

@cash_amount_bp.route('/amount/years/<year>', methods=['GET'])
def cash_amount_by_year(year):
    data = [0 for _ in range(12)]
    for receipt in db:
        current_date = datetime.datetime.strptime(receipt['date_closed'], "%Y-%m-%d %H:%M:%S")
        receipt_year = current_date.strftime('%Y')
        if receipt_year == year:
            receipt_month = int(current_date.strftime('%-m'))
            data[receipt_month-1] += receipt['total']
    return jsonify({ "data": data })
