
from backend.strategies.bot_strategy1 import Bot1
from backend.strategies.bot_strategy2 import Bot2
from backend.strategies.bot_strategy3 import Bot3
from backend.strategies.bot_strategy4 import Bot4
from backend.strategies.bot_strategy5 import Bot5
from backend.strategies.bot_strategy6 import Bot6
from backend.strategies.bot_strategy7 import Bot7
from backend.strategies.bot_strategy8 import Bot8
from backend.strategies.bot_strategy9 import Bot9
from backend.strategies.bot_strategy10 import Bot10
from backend.strategies.bot_strategy11 import Bot11
from backend.strategies.bot_strategy12 import Bot12
from backend.strategies.bot_strategy13 import Bot13
from backend.strategies.bot_strategy14 import Bot14
from backend.strategies.bot_strategy15 import Bot15
from backend.strategies.bot_strategy16 import Bot16
from backend.strategies.bot_strategy17 import Bot17
from backend.strategies.bot_strategy18 import Bot18
from backend.strategies.bot_strategy19 import Bot19
from backend.strategies.bot_strategy20 import Bot20
from backend.api.trading import execute_trade
import time

class TradingApp:
    def __init__(self):
        # Inicializando todas as estratégias de trading
        self.strategies = [
            Bot1(), Bot2(), Bot3(), Bot4(), Bot5(),
            Bot6(), Bot7(), Bot8(), Bot9(), Bot10(),
            Bot11(), Bot12(), Bot13(), Bot14(), Bot15(),
            Bot16(), Bot17(), Bot18(), Bot19(), Bot20()
        ]
        self.is_running = True

    def execute_strategy(self, bot_strategy):
        """Executa a estratégia de trading e realiza operações"""
        # Obtém o sinal de compra/venda
        signal = bot_strategy.generate_signal()
        if signal == "BUY":
            # Chama a função execute_trade para realizar a compra
            execute_trade(
                trade_type="BUY",
                amount=bot_strategy.trade_size,
                bot_name=bot_strategy.__class__.__name__,
            )
            bot_strategy.buy()
        elif signal == "SELL":
            # Chama a função execute_trade para realizar a venda
            execute_trade(
                trade_type="SELL",
                amount=bot_strategy.trade_size,
                bot_name=bot_strategy.__class__.__name__,
            )
            bot_strategy.sell()

    def start_trading(self):
        """Inicia a execução das estratégias"""
        while self.is_running:
            for bot_strategy in self.strategies:
                self.execute_strategy(bot_strategy)
                time.sleep(5)  # Intervalo entre execuções

    def stop_trading(self):
        """Interrompe a execução das estratégias"""
        self.is_running = False

if __name__ == "__main__":
    app = TradingApp()
    app.start_trading()
