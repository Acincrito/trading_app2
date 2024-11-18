# backend/strategies/bot7.py

# Estratégia de Escalonamento
# Compra e vende em múltiplos de um tamanho de operação base para tentar capturar oscilações de curto prazo.

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot7:
    def __init__(self, saldo_inicial=1000, base_trade_size=10, strategy_type="signal_based"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação base e tipo de estratégia.

        :param saldo_inicial: Saldo inicial do bot.
        :param base_trade_size: Tamanho base da operação.
        :param strategy_type: Tipo de estratégia ('signal_based', 'scaled_trading').
        """
        self.balance = saldo_inicial
        self.base_trade_size = base_trade_size
        self.strategy_type = strategy_type

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading com base no tipo escolhido.

        :param num_trades: Número de operações a serem realizadas.
        """
        for _ in range(num_trades):
            if self.strategy_type == "signal_based":
                self.signal_based_strategy()
            elif self.strategy_type == "scaled_trading":
                self.scaled_trading_strategy()
            else:
                print("Estratégia desconhecida.")
                break

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda."""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def signal_based_strategy(self):
        """Estratégia baseada em sinais aleatórios de compra e venda."""
        signal = self.generate_signal()
        print(f"Executando operação {signal} de {self.base_trade_size} unidades")

        if signal == 'BUY':
            self.buy(self.base_trade_size)
        elif signal == 'SELL':
            self.sell(self.base_trade_size)

    def scaled_trading_strategy(self):
        """Estratégia de compra e venda escalonada."""
        for i in range(1, 4):  # Escalonamento em 3 ordens
            trade_size = self.base_trade_size * i
            if self.balance < trade_size:
                print(f"Saldo insuficiente para executar operação escalonada de {trade_size} unidades.")
                break

            if i % 2 == 0:
                self.buy(trade_size)
            else:
                self.sell(trade_size)

    def buy(self, size):
        """Executa uma compra."""
        if self.balance >= size:
            self.balance -= size
            print(f"Compra executada de {size} unidades. Saldo restante: {self.balance}")
            self.record_operation('BUY', size)
        else:
            print(f"Saldo insuficiente para compra de {size} unidades. Operação cancelada.")

    def sell(self, size):
        """Executa uma venda."""
        self.balance += size
        print(f"Venda executada de {size} unidades. Saldo restante: {self.balance}")
        self.record_operation('SELL', size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot7",  # Nome do bot
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
    bot_signal_based = Bot7(saldo_inicial=1000, base_trade_size=10, strategy_type="signal_based")
    bot_signal_based.run(num_trades=5)

    print("\n---- Estratégia de Trading Escalonado ----")
    bot_scaled_trading = Bot7(saldo_inicial=1000, base_trade_size=10, strategy_type="scaled_trading")
    bot_scaled_trading.run(num_trades=1)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot7(saldo_inicial=1000, base_trade_size=10, strategy_type="signal_based")  # Corrige a classe para Bot7
    print("Bot Strategy Executando...")  # Exibe mensagem indicando início do bot
    bot.run(num_trades=10)  # Executa múltiplas operações
