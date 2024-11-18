# backend/strategies/bot2.py

# Estratégia de Tendência
from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot2:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="signal_based"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('signal_based', 'alternating', etc.)
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type
        self.last_signal = None  # Usado na estratégia 'alternating'

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading com base no tipo escolhido.

        :param num_trades: Número de operações a serem realizadas.
        """
        for _ in range(num_trades):
            if self.strategy_type == "signal_based":
                self.signal_based_strategy()
            elif self.strategy_type == "alternating":
                self.alternating_signal_strategy()
            else:
                print("Estratégia desconhecida.")
                break

    def generate_signal(self):
        """Gera sinal de compra ou venda aleatório."""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def signal_based_strategy(self):
        """Estratégia baseada em sinais aleatórios de compra e venda."""
        signal = self.generate_signal()
        print(f"Executando operação {signal} de {self.trade_size} unidades")
        
        if signal == 'BUY':
            self.buy(self.trade_size)
        elif signal == 'SELL':
            self.sell(self.trade_size)

    def alternating_signal_strategy(self):
        """Estratégia baseada em sinais alternados de compra e venda."""
        if self.last_signal is None:
            self.last_signal = 'BUY'

        print(f"Executando operação {self.last_signal} de {self.trade_size} unidades")
        
        if self.last_signal == 'BUY':
            self.buy(self.trade_size)
            self.last_signal = 'SELL'
        elif self.last_signal == 'SELL':
            self.sell(self.trade_size)
            self.last_signal = 'BUY'

    def buy(self, trade_size):
        """Executa uma compra."""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra executada. Saldo restante: {self.balance}")
            self.record_operation('BUY', trade_size)
        else:
            print(f"Saldo insuficiente para compra de {trade_size} unidades. Operação cancelada.")

    def sell(self, trade_size):
        """Executa uma venda."""
        self.balance += trade_size
        print(f"Venda executada. Saldo restante: {self.balance}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot2",  # Nome do bot
                trade_type=trade_type,
                amount=trade_size,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                robot_id=1  # ID do robô
            )
            db.add(operation)
            db.commit()
        except Exception as e:
            print(f"Erro ao gravar operação no banco de dados: {e}")
        finally:
            db.close()


# Exemplo de uso:
if __name__ == "__main__":
    print("---- Estratégia Baseada em Sinais ----")
    bot_signal_based = Bot2(saldo_inicial=1000, trade_size=10, strategy_type="signal_based")
    bot_signal_based.run(num_trades=5)

    print("\n---- Estratégia de Sinal Alternado ----")
    bot_alternating = Bot2(saldo_inicial=1000, trade_size=10, strategy_type="alternating")
    bot_alternating.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot2(saldo_inicial=1000, trade_size=10, strategy_type="signal_based")  # Corrige a classe para Bot2
    print("Bot Strategy Executando...")  # Exibe mensagem indicando início do bot
    bot.run(num_trades=10)  # Executa múltiplas operações
