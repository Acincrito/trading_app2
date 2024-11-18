# backend/__init__.py
from flask import Flask
from backend.api.trading import trading_bp

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Registrar Blueprint da API de trading
    app.register_blueprint(trading_bp, url_prefix='/api/trading')
    
    return app
