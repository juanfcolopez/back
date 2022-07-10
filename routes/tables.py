from flask import jsonify, Blueprint
from db.data import db
from aux.dates_validator import date_validator, date_in_range
tables_bp = Blueprint('routes-tables', __name__)

@tables_bp.route('/tables/<top>/<start>/<end>/', methods=['GET'])
def top_tables_most_used(top, start, end):
    tables = {}
    if date_validator(start, end):
        for receipt in db:
            if date_in_range(start, end, receipt['date_closed']):
                if receipt['table'] not in tables:
                    tables[receipt['table']] = 1
                elif receipt['table'] in tables: tables[receipt['table']] += 1
    #https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    reversed_sorted_tables = [*dict(sorted(tables.items(), key=lambda item: item[1], reverse=True)).keys()]
    top_tables = {}
    for index in range(int(top)):
        table_number = reversed_sorted_tables[index]
        top_tables[table_number] = {'Mesa': table_number, 'Utilizada': tables[table_number]}
    data = [*top_tables.values()]
    return jsonify({ "data": data })

@tables_bp.route('/tables/cash/<start>/<end>/', methods=['GET'])
def cash_by_table(start, end):
    tables = {}
    if date_validator(start, end):
        for receipt in db:
            if date_in_range(start, end, receipt['date_closed']):
                if receipt['table'] not in tables:
                    tables[receipt['table']] = receipt['total']
                elif receipt['table'] in tables: tables[receipt['table']] += receipt['total']
    data = []
    #https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_tables = [*dict(sorted(tables.items(), key=lambda item: item[0])).keys()]
    cash_by_table = []
    for table in sorted_tables:
        cash_by_table.append(tables[table])
    data.append(sorted_tables)
    data.append(cash_by_table)
    return jsonify({ "data": data })

@tables_bp.route('/tables/', methods=['GET'])
def total_tables():
    tables = []    
    for receipt in db:
        if receipt['table'] not in tables:
            tables.append(receipt['table'])
    data = [number + 1 for number in range(len(tables))]
    return jsonify({ "data": data })
