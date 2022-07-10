from math import prod
from flask import jsonify, Blueprint
from db.data import db
from aux.dates_validator import date_in_range, end_date_formatter, start_date_formatter, date_formatter, date_validator

products_bp = Blueprint('routes-products', __name__)

@products_bp.route('/products/sells/<category>/<start>/<end>', methods=['GET'])
def most_selling_by_category(category, start, end):
    names = []
    quantity = []
    total_sell = {}
    if date_validator(start, end):
        for receipt in db:
            if date_in_range(start, end, receipt['date_closed']):
                for product in receipt['products']:
                    if product['category'] == category:
                        if product['name'] not in names:
                            names.append(product['name'])
                            quantity.append(product['quantity'])
                            total_sell[product['name']] = {'Nombre': product['name'], 'Cantidad ($)': product['quantity']*product['price']}
                        else:
                            index = names.index(product['name'])
                            quantity[index] += product['quantity']
                            total_sell[names[index]]['Cantidad ($)'] += product['quantity']*product['price']
    data = [names, quantity, [*total_sell.values()]]
    return jsonify({ "data": data })

@products_bp.route('/products/categories', methods=['GET'])
def get_categories():
    categories = {}
    for receipt in db:
        for product in receipt['products']:
            if product['category'] not in categories:
                categories[product['category']] = {'value': product['category'], 'text': product['category']}
    return jsonify({"data": [*categories.values()]})