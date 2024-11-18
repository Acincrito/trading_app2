# backend/strategies/bot3.py

# Estratégia Baseada em Limites de Saldo

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot3:
    def __init__(self, saldo_inicial=1000, base_trade_size=10, strategy_type="signal_based", min_balance=800, max_balance=1200):
        """
        Inicializa o bot com saldo inicial, tamanho da operação base, tipo de estratégia, 
        e limites de saldo.

        :param saldo_inicial: Saldo inicial do bot.
        :param base_trade_size: Tamanho base da operação.
        :param strategy_type: Tipo de estratégia ('signal_based', 'balance_check').
        :param min_balance: Saldo mínimo para executar a operação.
        :param max_balance: Saldo máximo para executar a operação.
        """
        self.balance = saldo_inicial
        self.base_trade_size = base_trade_size
        self.strategy_type = strategy_type
        self.min_balance = min_balance
        self.max_balance = max_balance

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading com base no tipo escolhido.

        :param num_trades: Número de operações a serem realizadas.
        """
        for _ in range(num_trades):
            if self.strategy_type == "signal_based":
                self.signal_based_strategy()
            elif self.strategy_type == "balance_check":
                self.balance_check_strategy()
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

    def balance_check_strategy(self):
        """Estratégia que executa a operação somente se o saldo estiver dentro do limite."""
        if self.min_balance <= self.balance <= self.max_balance:
            print(f"Executando operação com saldo dentro dos limites.")
            self.buy(self.base_trade_size)
        else:
            print(f"Saldo fora dos limites ({self.balance}). Não houve operação.")

    def buy(self, size):
        """Executa uma compra."""
        if self.balance >= size:
            self.balance -= size
            print(f"Compra executada de {size} unidades. Saldo restante: {self.balance}")
            self.record_operation('BUY', size)
        else:
            print(f"Saldo insuficiente para compra. Operação cancelada. Saldo atual: {self.balance}")

    def sell(self, size):
        """Executa uma venda."""
        self.balance += size
        print(f"Venda executada de {size} unidades. Saldo restante: {self.balance}")
        self.record_operation('SELL', size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        with SessionLocal() as db:  # Usando 'with' para garantir o fechamento da conexão
            try:
                operation = Operation(
                    bot_name="Bot3",  # Nome do bot
                    trade_type=trade_type,
                    amount=trade_size,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    robot_id=1  # ID do robô
                )
                db.add(operation)
                db.commit()
            except Exception as e:
                print(f"Erro ao gravar operação no banco de dados: {e}")


# Exemplo de uso:
if __name__ == "__main__":
    print("---- Estratégia Baseada em Sinais ----")
    bot_signal_based = Bot3(saldo_inicial=1000, base_trade_size=10, strategy_type="signal_based")
    bot_signal_based.run(num_trades=5)

    print("\n---- Estratégia com Verificação de Saldo ----")
    bot_balance_check = Bot3(saldo_inicial=1000, base_trade_size=10, strategy_type="balance_check")
    bot_balance_check.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot3(saldo_inicial=1000, base_trade_size=10, strategy_type="signal_based")  # Corrige a classe para Bot3
    print("Bot Strategy Executando...")  # Exibe uma mensagem indicando que o bot foi iniciado
    bot.run(num_trades=5)  # Chama o método run() que executa a lógica de trading (compra ou venda)
