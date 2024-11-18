# backend/strategies/bot18.py

# Estratégia de Compra Decrescente
# Diminui o valor da operação progressivamente para minimizar perdas em sequência.


from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot18:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="basic"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('basic', 'decreasing').
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading com base no tipo escolhido.

        :param num_trades: Número de operações a serem realizadas.
        """
        for i in range(num_trades):
            print(f"\nOperação {i + 1} de {num_trades}")
            if self.strategy_type == "basic":
                self.basic_strategy()
            elif self.strategy_type == "decreasing":
                self.decreasing_strategy()
            else:
                print("Estratégia desconhecida.")
                break

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda."""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def basic_strategy(self):
        """Estratégia básica de compra e venda."""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy(self.trade_size)
        elif signal == 'SELL':
            self.sell(self.trade_size)

    def decreasing_strategy(self):
        """Estratégia com compra progressivamente decrescente."""
        if self.trade_size <= 0:
            print("Tamanho da operação chegou ao mínimo. Estratégia encerrada.")
            return

        if self.balance >= self.trade_size:
            self.buy(self.trade_size)
            self.trade_size = max(1, self.trade_size - 1)  # Reduz progressivamente o tamanho da operação
            print(f"Tamanho da operação reduzido. Novo tamanho: {self.trade_size}")
        else:
            print("Saldo insuficiente para executar a estratégia decrescente. Operação encerrada.")

    def buy(self, trade_size):
        """Executa uma compra."""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra de {trade_size} unidades. Saldo: {self.balance}")
            self.record_operation('BUY', trade_size)
        else:
            print(f"Saldo insuficiente para compra de {trade_size}. Operação cancelada.")

    def sell(self, trade_size):
        """Executa uma venda."""
        self.balance += trade_size
        print(f"Venda de {trade_size} unidades. Saldo: {self.balance}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot18",  # Nome do bot
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
    print("---- Estratégia Básica ----")
    bot_basic = Bot18(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run(num_trades=5)

    print("\n---- Estratégia Decrescente ----")
    bot_decreasing = Bot18(saldo_inicial=1000, trade_size=10, strategy_type="decreasing")
    bot_decreasing.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot18(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    print("Bot Strategy Executando...")
    bot.run(num_trades=10)
