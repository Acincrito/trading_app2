# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta'
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
    BOT_CONFIG = {
        'bot1': {'max_trades': 5, 'risk_level': 'medium'},
        'bot2': {'max_trades': 10, 'risk_level': 'high'},
        # Adicione mais configurações conforme necessário
    }
