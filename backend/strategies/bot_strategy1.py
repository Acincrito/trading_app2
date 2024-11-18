# backend/strategies/bot_strategy1.py
# Importando a classe Bot1 que será usada na estratégia
from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot1:
    def __init__(self, bot_name="BotStrategy1", trade_size=10, initial_balance=1000, log_operations=True):
        """
        Inicializa o bot genérico com parâmetros configuráveis.
        
        :param bot_name: Nome do bot.
        :param trade_size: Tamanho de cada operação.
        :param initial_balance: Saldo inicial do bot.
        :param log_operations: Define se as operações serão exibidas no console.
        """
        self.bot_name = bot_name
        self.balance = initial_balance
        self.trade_size = trade_size
        self.log_operations = log_operations

    def run(self):
        """
        Executa a estratégia de trading.
        Com base no sinal gerado, realiza uma operação de compra ou venda.
        """
        signal = self.generate_signal()
        if signal == 'BUY':
            self.buy()
        elif signal == 'SELL':
            self.sell()

    def generate_signal(self):
        """
        Gera um sinal de compra ou venda de forma aleatória.
        
        :return: 'BUY' ou 'SELL'.
        """
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def buy(self):
        """
        Executa uma operação de compra, caso o saldo seja suficiente.
        """
        if self.balance >= self.trade_size:
            self.balance -= self.trade_size
            self.record_operation('BUY')
            if self.log_operations:
                print(f"[{self.bot_name}] Compra realizada. Saldo atual: {self.balance}")
        else:
            if self.log_operations:
                print(f"[{self.bot_name}] Saldo insuficiente para realizar compra.")

    def sell(self):
        """
        Executa uma operação de venda, aumentando o saldo.
        """
        self.balance += self.trade_size
        self.record_operation('SELL')
        if self.log_operations:
            print(f"[{self.bot_name}] Venda realizada. Saldo atual: {self.balance}")

    def record_operation(self, trade_type):
        """
        Grava os detalhes da operação no banco de dados.
        
        :param trade_type: Tipo da operação (BUY ou SELL).
        """
        try:
            # Usando o context manager para garantir que a sessão seja fechada automaticamente
            with SessionLocal() as db:
                operation = Operation(
                    bot_name=self.bot_name,
                    trade_type=trade_type,
                    amount=self.trade_size,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    robot_id=self.bot_name  # Nome do bot usado como identificador
                )
                db.add(operation)
                db.commit()
        except Exception as e:
            if self.log_operations:
                print(f"Erro ao gravar operação para {self.bot_name}: {e}")

# Função que executa a estratégia do Bot1
def execute():
    """
    Função para executar a estratégia do Bot 1.
    Cria uma instância do Bot1 e executa a função run() para realizar as operações de compra e venda.
    """
    bot1 = Bot1()  # Cria uma instância do bot
    print("Bot Strategy 1 Executando...")  # Exibe uma mensagem indicando que o bot foi iniciado
    bot1.run()  # Chama o método run() que executa a lógica de trading (compra ou venda)
