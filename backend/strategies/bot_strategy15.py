# backend/strategies/bot15.py

# Estratégia de Alta Frequência
# Executa operações consecutivas para capturar micro variações de preço.

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot15:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="basic"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot
        :param trade_size: Tamanho da operação
        :param strategy_type: Tipo de estratégia ('basic', 'high_frequency' ou outra)
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type

    def run(self, num_trades=10):
        """Executa a estratégia de trading com base no tipo escolhido"""
        for _ in range(num_trades):
            if self.balance < self.trade_size:
                print("Saldo insuficiente para continuar as operações. Execução encerrada.")
                break

            if self.strategy_type == "basic":
                self.basic_strategy()
            elif self.strategy_type == "high_frequency":
                self.high_frequency_strategy()
            else:
                print("Estratégia desconhecida.")
                break

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda"""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def basic_strategy(self):
        """Estratégia básica de compra e venda"""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy(self.trade_size)
        elif signal == 'SELL':
            self.sell(self.trade_size)

    def high_frequency_strategy(self):
        """Estratégia de alta frequência (executa múltiplas compras)"""
        for _ in range(10):  # Executa 10 compras em sequência, mas com saldo controlado
            if self.balance < self.trade_size:
                print("Saldo insuficiente para executar mais compras na estratégia de alta frequência.")
                break
            self.buy(self.trade_size)

    def buy(self, trade_size):
        """Executa uma compra"""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra executada de {trade_size} unidades. Saldo restante: {self.balance:.2f}")
            self.record_operation('BUY', trade_size)
        else:
            print("Saldo insuficiente para executar a compra.")

    def sell(self, trade_size):
        """Executa uma venda"""
        self.balance += trade_size
        print(f"Venda executada de {trade_size} unidades. Saldo restante: {self.balance:.2f}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados"""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot15",  # Nome do bot
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
    # Estratégia básica de compra e venda
    bot_basic = Bot15(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run(num_trades=5)

    print("\n---- Operações com Estratégia de Alta Frequência ----")
    # Estratégia de alta frequência
    bot_high_freq = Bot15(saldo_inicial=1000, trade_size=1, strategy_type="high_frequency")
    bot_high_freq.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot15(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    print("Bot Strategy Executando...")
    bot.run(num_trades=10)
