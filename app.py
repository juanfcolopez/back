from flask import Flask
from flask_cors import CORS
from routes.payments import payments_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(payments_bp)
