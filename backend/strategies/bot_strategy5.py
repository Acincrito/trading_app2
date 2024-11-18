# backend/strategies/bot5.py

# Estratégia de Reversão
from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot5:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="random"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('random', 'gain_loss').
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.previous_result = None  # Usado na estratégia 'gain_loss'
        self.strategy_type = strategy_type

    def run(self):
        """Executa a estratégia de trading com base no tipo escolhido."""
        if self.strategy_type == "random":
            self.random_strategy()
        elif self.strategy_type == "gain_loss":
            self.gain_loss_strategy()
        else:
            print("Estratégia desconhecida.")

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

    def gain_loss_strategy(self):
        """Estratégia baseada no resultado anterior: 
        Se ganhou, realiza a venda. Se perdeu, realiza a compra.
        """
        print(f"Resultado anterior: {self.previous_result}")

        if self.previous_result == "gain":
            self.sell(self.trade_size)
        elif self.previous_result == "loss":
            self.buy(self.trade_size)
        else:
            print("Nenhum resultado anterior. Iniciando com compra.")
            self.buy(self.trade_size)  # Inicializa com uma compra se for a primeira operação

    def buy(self, trade_size):
        """Executa uma compra."""
        self.balance -= trade_size
        self.previous_result = "loss"  # Resultado após compra é "loss"
        print(f"Compra de {trade_size} unidades. Saldo: {self.balance}")
        self.record_operation('BUY', trade_size)

    def sell(self, trade_size):
        """Executa uma venda."""
        self.balance += trade_size
        self.previous_result = "gain"  # Resultado após venda é "gain"
        print(f"Venda de {trade_size} unidades. Saldo: {self.balance}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        db = SessionLocal()
        operation = Operation(
            bot_name="Bot5",  # Nome do bot
            trade_type=trade_type,
            amount=trade_size,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            robot_id=1  # ID do robô
        )
        db.add(operation)
        db.commit()
        db.close()

# Exemplo de uso:
if __name__ == "__main__":
    # Estratégia aleatória
    bot_random = Bot5(saldo_inicial=1000, trade_size=10, strategy_type="random")
    bot_random.run()

    print("\n---- Estratégia Ganho/Perda ----\n")

    # Estratégia baseada em ganho/perda anterior
    bot_gain_loss = Bot5(saldo_inicial=1000, trade_size=10, strategy_type="gain_loss")
    bot_gain_loss.run()

def execute():
    """
    Função para executar a estratégia do Bot 
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot5(saldo_inicial=1000, trade_size=10, strategy_type="gain_loss")  # Correção para Bot5
    print("Bot Strategy Executando...")  # Exibe uma mensagem indicando que o bot foi iniciado
    bot.run()  # Chama o método run() que executa a lógica de trading (compra ou venda)
