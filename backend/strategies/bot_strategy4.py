# backend/strategies/bot4.py

# Estratégia de Média Móvel Simples

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random


class Bot4:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="random"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('random', 'moving_average').
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type
        self.price_history = [100]  # Histórico de preços para a estratégia de média móvel

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
            elif self.strategy_type == "moving_average":
                self.moving_average_strategy()
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

        if signal == 'BUY' and self.balance >= self.trade_size:
            self.buy(self.trade_size)
        elif signal == 'SELL':
            self.sell(self.trade_size)
        else:
            print("Saldo insuficiente para executar a operação de compra.")

    def moving_average_strategy(self):
        """Estratégia baseada na média móvel dos preços históricos."""
        current_price = random.uniform(95, 105)  # Preço simulado
        self.price_history.append(current_price)
        moving_average = sum(self.price_history[-5:]) / min(5, len(self.price_history))
        
        print(f"Preço atual: {current_price:.2f}, Média Móvel: {moving_average:.2f}")

        if current_price > moving_average and self.balance >= self.trade_size:
            self.buy(self.trade_size)
        else:
            self.sell(self.trade_size)

    def buy(self, trade_size):
        """Executa uma compra."""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra de {trade_size} unidades. Saldo: {self.balance:.2f}")
            self.record_operation('BUY', trade_size)
        else:
            print("Saldo insuficiente para executar a compra.")

    def sell(self, trade_size):
        """Executa uma venda."""
        self.balance += trade_size
        print(f"Venda de {trade_size} unidades. Saldo: {self.balance:.2f}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot4",  # Nome do bot
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
    print("---- Estratégia Aleatória ----")
    bot_random = Bot4(saldo_inicial=1000, trade_size=10, strategy_type="random")
    bot_random.run(num_trades=5)

    print("\n---- Estratégia de Média Móvel ----")
    bot_ma = Bot4(saldo_inicial=1000, trade_size=10, strategy_type="moving_average")
    bot_ma.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot.
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot4(saldo_inicial=1000, trade_size=10, strategy_type="random")
    print("Bot Strategy Executando...")
    bot.run(num_trades=10)
