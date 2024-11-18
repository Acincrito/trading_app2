# backend/strategies/bot9.py

# Estratégia de Stop Loss e Take Profit
# Define um limite de perdas e ganhos antes de decidir parar a execução.


# Exemplo de bot_strategy.py

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot9:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="basic", stop_loss=950, take_profit=1050):
        """
        Inicializa o bot com saldo inicial, tamanho da operação, e o tipo de estratégia a ser utilizada.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('basic', 'with_stop_loss').
        :param stop_loss: Limite de stop loss.
        :param take_profit: Limite de take profit.
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def run(self):
        """Executa a estratégia de trading com base no tipo escolhido."""
        if self.balance <= self.stop_loss:
            print("Stop Loss atingido. Operações encerradas.")
            return
        elif self.balance >= self.take_profit:
            print("Take Profit atingido. Operações encerradas.")
            return

        if self.strategy_type == "basic":
            self.basic_strategy()
        elif self.strategy_type == "with_stop_loss":
            self.strategy_with_stop_loss()
        else:
            print("Estratégia desconhecida.")

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

    def strategy_with_stop_loss(self):
        """Estratégia com Stop Loss e Take Profit."""
        if self.balance <= self.stop_loss:
            print("Stop Loss atingido. Operações encerradas.")
            return
        elif self.balance >= self.take_profit:
            print("Take Profit atingido. Operações encerradas.")
            return
        else:
            signal = self.generate_signal()
            print(f"Executando operação com sinal: {signal}")
            if signal == 'BUY':
                self.buy(self.trade_size)
            elif signal == 'SELL':
                self.sell(self.trade_size)

    def buy(self, trade_size):
        """Executa uma compra."""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra de {trade_size} unidades. Saldo: {self.balance}")
            self.record_operation('BUY', trade_size)
        else:
            print(f"Saldo insuficiente para realizar a compra de {trade_size} unidades.")

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
                bot_name="Bot9",  # Nome do bot
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
    # Estratégia básica de compra e venda
    bot_basic = Bot9(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run()

    print("\n---- Operações com Stop Loss e Take Profit ----\n")

    # Estratégia com Stop Loss e Take Profit
    bot_with_stop_loss = Bot9(saldo_inicial=1000, trade_size=10, strategy_type="with_stop_loss", stop_loss=950, take_profit=1050)
    bot_with_stop_loss.run()


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot9(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    print("Bot Strategy Executando...")
    bot.run()
