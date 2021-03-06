from flask import Flask
from flask_cors import CORS
from routes.payments import payments_bp
from routes.products import products_bp
from routes.workers import workers_bp
from routes.cash_amount import cash_amount_bp
from routes.tables import tables_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(payments_bp)
app.register_blueprint(products_bp)
app.register_blueprint(workers_bp)
app.register_blueprint(cash_amount_bp)
app.register_blueprint(tables_bp)
