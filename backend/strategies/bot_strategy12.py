# backend/strategies/bot12.py

# Estratégia de Alavancagem
# Dobra o tamanho da operação após um ganho, arriscando mais para aumentar o lucro.


from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot12:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="random"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot.
        :param trade_size: Tamanho da operação.
        :param strategy_type: Tipo de estratégia ('random', 'leveraged').
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type

    def run(self):
        """Executa a estratégia de trading com base no tipo escolhido."""
        if self.strategy_type == "random":
            self.random_strategy()
        elif self.strategy_type == "leveraged":
            self.leveraged_strategy()
        else:
            print("Estratégia desconhecida.")

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda."""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def random_strategy(self):
        """Estratégia baseada em sinais aleatórios de compra e venda."""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if self.balance > 500:  # Condição para definir o tamanho da operação
            trade_size = self.balance * 0.05  # 5% do saldo
        else:
            trade_size = self.balance * 0.10  # 10% do saldo

        if signal == 'BUY':
            self.buy(trade_size)
        elif signal == 'SELL':
            self.sell(trade_size)

    def leveraged_strategy(self):
        """Estratégia de compra alavancada: dobra o tamanho da operação se o saldo for maior que 1000."""
        print(f"Saldo atual: {self.balance}")
        
        if self.balance > 1000:
            original_trade_size = self.trade_size  # Salvar o tamanho original da operação
            self.trade_size *= 2  # Alavanca a operação
            print(f"Tamanho da operação alavancado para {self.trade_size}.")
            self.buy(self.trade_size)
            print(f"Operação alavancada: de {original_trade_size} para {self.trade_size}")
        else:
            print(f"Saldo insuficiente para alavancagem. Executando operação com {self.trade_size}.")
            self.buy(self.trade_size)

    def buy(self, trade_size):
        """Executa uma compra.""" 
        if self.balance >= trade_size:  # Verificação de saldo suficiente
            self.balance -= trade_size
            print(f"Compra de {trade_size} unidades. Saldo: {self.balance}")
            self.record_operation('BUY', trade_size)
        else:
            print("Saldo insuficiente para comprar.")

    def sell(self, trade_size):
        """Executa uma venda."""
        self.balance += trade_size
        print(f"Venda de {trade_size} unidades. Saldo: {self.balance}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados."""
        try:
            db = SessionLocal()
            operation = Operation(
                bot_name="Bot12",  # Nome do bot
                trade_type=trade_type,
                amount=trade_size,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                robot_id=1  # ID do robô
            )
            db.add(operation)
            db.commit()
            db.close()
        except Exception as e:
            print(f"Erro ao gravar a operação no banco de dados: {e}")

# Exemplo de uso:
if __name__ == "__main__":
    # Estratégia aleatória
    bot_random = Bot12(saldo_inicial=1000, trade_size=10, strategy_type="random")
    bot_random.run()

    print("\n---- Estratégia Alavancada ----\n")

    # Estratégia de alavancagem
    bot_leveraged = Bot12(saldo_inicial=1000, trade_size=10, strategy_type="leveraged")
    bot_leveraged.run()

def execute():
    """
    Função para executar a estratégia do Bot 
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot12(saldo_inicial=1000, trade_size=10, strategy_type="leveraged")  # Correção para Bot12
    print("Bot Strategy Executando...")  # Exibe uma mensagem indicando que o bot foi iniciado
    bot.run()  # Chama o método run() que executa a lógica de trading (compra ou venda)
