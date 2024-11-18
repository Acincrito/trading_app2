# backend/strategies/bot8.py

# Estratégia de Volatilidade
# Opera baseado em simulações de alta volatilidade, comprando se o saldo anterior foi positivo e vendendo caso contrário.

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot8:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="random"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('random', 'volatility').
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
            if self.balance < self.trade_size:
                print("Saldo insuficiente para continuar as operações. Execução encerrada.")
                break

            if self.strategy_type == "random":
                self.random_strategy()
            elif self.strategy_type == "volatility":
                self.volatility_strategy()
            else:
                print("Estratégia desconhecida.")
                break

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda."""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def random_strategy(self):
        """Estratégia baseada em sinais aleatórios de compra e venda."""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy(self.trade_size)
        elif signal == 'SELL':
            self.sell(self.trade_size)

    def volatility_strategy(self):
        """Estratégia baseada na volatilidade do mercado."""
        volatility = random.uniform(0.9, 1.1)  # Simula a volatilidade do mercado
        print(f"Volatilidade do mercado: {volatility:.2f}")

        if volatility > 1.05:
            print("Alta volatilidade detectada. Executando compra.")
            self.buy(self.trade_size)
        elif volatility < 0.95:
            print("Baixa volatilidade detectada. Executando venda.")
            self.sell(self.trade_size)
        else:
            print("Volatilidade neutra. Nenhuma operação executada.")

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
                bot_name="Bot8",  # Nome do bot
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
    print("---- Estratégia de Sinais Aleatórios ----")
    bot_random = Bot8(saldo_inicial=1000, trade_size=10, strategy_type="random")
    bot_random.run(num_trades=5)

    print("\n---- Estratégia Baseada em Volatilidade ----")
    bot_volatility = Bot8(saldo_inicial=1000, trade_size=10, strategy_type="volatility")
    bot_volatility.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot8(saldo_inicial=1000, trade_size=10, strategy_type="random")
    print("Bot Strategy Executando...")
    bot.run(num_trades=10)
