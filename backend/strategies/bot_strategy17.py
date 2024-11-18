# backend/strategies/bot17.py

# Estratégia de Risco Progressivo
# Aumenta o tamanho do trade progressivamente após cada ganho consecutivo.


from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot17:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="random"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('random', 'progressive_risk').
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type
        self.gain_streak = 0  # Usado para o risco progressivo

    def run(self, num_trades=10):
        """
        Executa a estratégia de trading com base no tipo escolhido.
        :param num_trades: Número de operações a serem realizadas.
        """
        for _ in range(num_trades):
            if self.strategy_type == "random":
                self.random_strategy()
            elif self.strategy_type == "progressive_risk":
                self.progressive_risk_strategy()
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

    def progressive_risk_strategy(self):
        """Estratégia com risco progressivo: aumenta o tamanho da operação após vitórias consecutivas."""
        signal = self.generate_signal()
        print(f"Operação com sinal: {signal} | Sequência de ganhos: {self.gain_streak}")

        # Define o tamanho da operação com base na sequência de vitórias
        trade_size = self.trade_size + (self.gain_streak * 5)
        
        if signal == 'BUY':
            if self.buy(trade_size):
                self.gain_streak += 1
            else:
                self.gain_streak = 0
        elif signal == 'SELL':
            if self.sell(trade_size):
                self.gain_streak += 1
            else:
                self.gain_streak = 0

    def buy(self, trade_size):
        """Executa uma compra."""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra de {trade_size} unidades. Saldo: {self.balance}")
            self.record_operation('BUY', trade_size)
            return True
        else:
            print("Saldo insuficiente para a compra.")
            return False

    def sell(self, trade_size):
        """Executa uma venda."""
        self.balance += trade_size
        print(f"Venda de {trade_size} unidades. Saldo: {self.balance}")
        self.record_operation('SELL', trade_size)
        return True

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot17",  # Nome do bot
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
    bot_random = Bot17(saldo_inicial=1000, trade_size=10, strategy_type="random")
    bot_random.run(num_trades=5)

    print("\n---- Estratégia de Risco Progressivo ----")
    bot_progressive = Bot17(saldo_inicial=1000, trade_size=10, strategy_type="progressive_risk")
    bot_progressive.run(num_trades=5)


def execute():
    """
    Função para executar a estratégia do Bot. 
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot17(saldo_inicial=1000, trade_size=10, strategy_type="random")  # Corrige a classe
    print("Bot Strategy Executando...")  # Mensagem de inicialização
    bot.run(num_trades=10)  # Executa múltiplas operações
