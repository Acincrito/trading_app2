# /backend/config/config.py

# Configurações gerais do aplicativo
CONFIG = {
    "broker_urls": {
        "iq_option": "https://api.iqoption.com",
        "metatrader": "https://api.metatrader.com",
        "binance": "https://api.binance.com",
    },
    "api_keys": {
        "iq_option": "your_iq_option_api_key_here",
        "metatrader": "your_metatrader_api_key_here",
        "binance": "your_binance_api_key_here",
    },
    "trading_strategies": {
        "moving_average": {
            "enabled": True,
            "parameters": {
                "short_period": 5,
                "long_period": 20,
                "threshold": 0.02  # Exemplo de limiar para sinal de compra/venda
            }
        },
        "rsi_strategy": {
            "enabled": True,
            "parameters": {
                "rsi_period": 14,
                "overbought_threshold": 70,
                "oversold_threshold": 30
            }
        }
    },
    "order_precision": {
        "iq_option": 0.01,  # Tamanho mínimo de ordem para IQ Option
        "binance": 0.0001,  # Tamanho mínimo de ordem para Binance
        "metatrader": 0.01,  # Tamanho mínimo de ordem para MetaTrader
    },
    "logging": {
        "enabled": True,
        "level": "INFO",  # Níveis: DEBUG, INFO, WARNING, ERROR
        "log_file": "trader_app.log",
    },
    "trade_config": {
        "default_trade_size": 10,  # Tamanho padrão para cada operação
        "stop_loss_percentage": 0.02,  # Stop loss em 2%
        "take_profit_percentage": 0.05,  # Take profit em 5%
        "max_consecutive_losses": 3,  # Número máximo de perdas consecutivas permitidas
        "max_consecutive_wins": 5,  # Número máximo de vitórias consecutivas permitidas
    },
    "notification_config": {
        "enabled": True,
        "email": "your_email@example.com",  # Email para notificações
        "sms": "+1234567890",  # Número de telefone para notificações SMS
    }
}
