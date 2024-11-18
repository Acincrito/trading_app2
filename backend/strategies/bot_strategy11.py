# backend/strategies/bot11.py

# Estratégia de Contrato Fixo
# Opera com um valor fixo, simulando contratos com valor e risco constantes.

from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot11:
    def __init__(self, saldo_inicial=1000, trade_size=10, contract_value=50, strategy_type="basic"):
        """
        Inicializa o bot com saldo inicial, tamanho da operação, valor do contrato e tipo de estratégia.
        
        :param saldo_inicial: Saldo inicial do bot
        :param trade_size: Tamanho da operação para estratégias de compra e venda
        :param contract_value: Valor do contrato para estratégia de execução de contratos
        :param strategy_type: Tipo de estratégia ('basic', 'contract_based')
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.contract_value = contract_value
        self.strategy_type = strategy_type

    def run(self):
        """Executa a estratégia de trading de acordo com o tipo especificado"""
        if self.strategy_type == "basic":
            self.basic_strategy()
        elif self.strategy_type == "contract_based":
            self.contract_based_strategy()
        else:
            print("Estratégia desconhecida.")

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda"""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def basic_strategy(self):
        """Estratégia básica de compra ou venda"""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy()
        elif signal == 'SELL':
            self.sell()

    def contract_based_strategy(self):
        """Estratégia baseada em contratos: executa um contrato dependendo do saldo"""
        if self.check_signal():
            self.trade_contract()

    def check_signal(self):
        """Verifica a condição para executar o contrato (exemplo: saldo suficiente)"""
        return self.balance > self.contract_value  # Verifica se o saldo é suficiente para um contrato

    def buy(self):
        """Executa uma compra e registra a operação"""
        if self.balance >= self.trade_size:  # Verifica se há saldo suficiente
            self.balance -= self.trade_size
            print(f"Compra executada. Tamanho da operação: {self.trade_size}. Saldo restante: {self.balance}")
            self.record_operation('BUY')
        else:
            print(f"Saldo insuficiente para realizar a compra de {self.trade_size}.")

    def sell(self):
        """Executa uma venda e registra a operação"""
        self.balance += self.trade_size
        print(f"Venda executada. Tamanho da operação: {self.trade_size}. Saldo restante: {self.balance}")
        self.record_operation('SELL')

    def trade_contract(self):
        """Executa um contrato e atualiza o saldo"""
        if self.balance >= self.contract_value:  # Verifica se há saldo suficiente para o contrato
            self.balance -= self.contract_value
            print(f"Contrato de {self.contract_value} executado. Saldo restante: {self.balance}")
            self.record_operation('CONTRACT')
        else:
            print(f"Saldo insuficiente para executar contrato de {self.contract_value}.")

    def record_operation(self, trade_type):
        """Grava a operação no banco de dados"""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot11",  # Nome do bot
                trade_type=trade_type,
                amount=self.trade_size if trade_type != 'CONTRACT' else self.contract_value,
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
    # Estratégia básica de compra e venda
    bot_basic = Bot11(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run()

    print("\n---- Operações com Contratos ----\n")

    # Estratégia baseada em contratos
    bot_contract = Bot11(saldo_inicial=1500, contract_value=50, strategy_type="contract_based")
    bot_contract.run()

def execute():
    """
    Função para executar a estratégia do Bot 
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot11(saldo_inicial=1000, trade_size=10, strategy_type="basic")  # Corrigido para Bot11
    print("Bot Strategy Executando...")  # Exibe uma mensagem indicando que o bot foi iniciado
    bot.run()  # Chama o método run() que executa a lógica de trading (compra ou venda)
