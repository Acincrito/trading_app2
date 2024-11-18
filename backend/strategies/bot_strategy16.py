# backend/strategies/bot16.py

# Estratégia de Diversificação
# Divide o saldo em várias operações menores para mitigar o risco.

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot16:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="basic"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('basic', 'diversified', 'progressive').
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type
        self.gain_streak = 0  # Para estratégias progressivas

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading de acordo com o tipo especificado.

        :param num_trades: Número de operações a serem realizadas.
        """
        for i in range(num_trades):
            print(f"\nOperação {i + 1} de {num_trades}")
            if self.balance < self.trade_size:
                print("Saldo insuficiente para continuar as operações. Execução encerrada.")
                break

            if self.strategy_type == "basic":
                self.basic_strategy()
            elif self.strategy_type == "diversified":
                self.diversified_strategy()
            elif self.strategy_type == "progressive":
                self.progressive_strategy()
            else:
                print("Estratégia desconhecida.")
                break

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda."""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def basic_strategy(self):
        """Estratégia básica de compra ou venda."""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy()
        elif signal == 'SELL':
            self.sell()

    def diversified_strategy(self):
        """Estratégia de diversificação: realiza várias compras com diferentes tamanhos."""
        for i in range(1, 6):  # Diversificação em 5 compras consecutivas
            trade_size = self.trade_size * i
            if self.balance >= trade_size:
                self.buy(trade_size)
            else:
                print(f"Saldo insuficiente para compra de {trade_size}. Operação cancelada.")
                break

    def progressive_strategy(self):
        """Estratégia progressiva: aumenta o tamanho da operação a cada ganho."""
        if self.gain_streak > 0:
            self.trade_size = min(self.trade_size + (self.gain_streak * 5), self.balance)

        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy()
            self.gain_streak += 1  # Incrementa sequência de ganhos
        elif signal == 'SELL':
            self.sell()
            self.gain_streak = 0  # Reseta a sequência de ganhos

    def buy(self, trade_size=None):
        """Executa uma compra e registra a operação."""
        trade_size = trade_size if trade_size else self.trade_size

        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra executada. Tamanho da operação: {trade_size}. Saldo restante: {self.balance}")
            self.record_operation('BUY', trade_size)
        else:
            print(f"Saldo insuficiente para compra de {trade_size}. Operação cancelada.")

    def sell(self):
        """Executa uma venda e registra a operação."""
        self.balance += self.trade_size
        print(f"Venda executada. Tamanho da operação: {self.trade_size}. Saldo restante: {self.balance}")
        self.record_operation('SELL', self.trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot16",  # Nome do bot
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
    bot_basic = Bot16(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run(num_trades=5)

    print("\n---- Operações com Diversificação ----\n")
    bot_diversified = Bot16(saldo_inicial=1000, trade_size=5, strategy_type="diversified")
    bot_diversified.run(num_trades=5)

    print("\n---- Operações com Risco Progressivo ----\n")
    bot_progressive = Bot16(saldo_inicial=1000, trade_size=5, strategy_type="progressive")
    bot_progressive.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot16(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    print("Bot Strategy Executando...")
    bot.run(num_trades=10)
