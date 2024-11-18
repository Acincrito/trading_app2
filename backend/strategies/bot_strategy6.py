# backend/strategies/bot6.py

# Estratégia de Martingale

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot6:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="basic"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot
        :param trade_size: Tamanho da operação
        :param strategy_type: Tipo de estratégia ('basic' ou 'martingale')
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.base_trade_size = trade_size
        self.current_trade_size = trade_size
        self.strategy_type = strategy_type

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading com base no tipo escolhido.

        :param num_trades: Número de operações a serem realizadas.
        """
        for _ in range(num_trades):
            if self.strategy_type == "basic":
                self.basic_strategy()
            elif self.strategy_type == "martingale":
                self.martingale_strategy()
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
            self.buy()
        elif signal == 'SELL':
            self.sell()

    def martingale_strategy(self):
        """Estratégia de Martingale - dobra a operação em caso de perda."""
        if self.check_loss():
            self.current_trade_size *= 2  # Dobra o tamanho da operação em caso de perda
            print(f"Perda detectada, aumentando o tamanho da operação para {self.current_trade_size}")
        else:
            self.current_trade_size = self.base_trade_size  # Retorna ao valor base após vitória
        
        signal = self.generate_signal()
        if signal == 'BUY':
            self.buy()
        else:
            self.sell()

    def buy(self):
        """Executa uma compra."""
        if self.balance >= self.current_trade_size:
            self.balance -= self.current_trade_size
            print(f"Compra executada. Tamanho da operação: {self.current_trade_size}. Saldo restante: {self.balance}")
            self.record_operation('BUY')
        else:
            print(f"Saldo insuficiente para compra de {self.current_trade_size}. Operação cancelada.")

    def sell(self):
        """Executa uma venda."""
        self.balance += self.current_trade_size
        print(f"Venda executada. Tamanho da operação: {self.current_trade_size}. Saldo restante: {self.balance}")
        self.record_operation('SELL')

    def check_loss(self):
        """
        Verifica se houve perda na operação anterior.
        Retorna True se o saldo atual for inferior ao saldo após a última operação.
        """
        return self.balance < (self.base_trade_size + self.trade_size)

    def record_operation(self, trade_type):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot6",  # Nome do bot
                trade_type=trade_type,
                amount=self.current_trade_size,
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
    bot_basic = Bot6(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run(num_trades=5)

    print("\n---- Estratégia Martingale ----")
    bot_martingale = Bot6(saldo_inicial=1000, trade_size=10, strategy_type="martingale")
    bot_martingale.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot6(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    print("Bot Strategy Executando...")
    bot.run(num_trades=10)
