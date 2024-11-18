# backend/strategies/bot19.py

# Estratégia Combinada de Alavancagem e Stop Loss com Contratos Variáveis
# Este bot mistura uma abordagem de alavancagem, onde aumenta o tamanho do trade após ganhos consecutivos, 
# com limites de stop loss e take profit para gerenciar riscos. Além disso, 
# ele utiliza contratos de valor fixo, variando o número de contratos conforme as condições de saldo.




from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random

class Bot19:
    def __init__(self, saldo_inicial=1000, trade_size=10, strategy_type="basic", stop_loss=900, take_profit=1100):
        """
        Inicializa o bot com saldo inicial, tamanho da operação, tipo de estratégia e limites de stop loss e take profit.
        
        :param saldo_inicial: Saldo inicial do bot
        :param trade_size: Tamanho da operação
        :param strategy_type: Tipo de estratégia ('basic', 'advanced')
        :param stop_loss: Limite de perda para stop loss
        :param take_profit: Limite de lucro para take profit
        """
        self.balance = saldo_inicial
        self.trade_size = trade_size
        self.strategy_type = strategy_type
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.gain_streak = 0  # Utilizado para o controle de sequência de ganhos

    def run(self):
        """Executa a estratégia de trading com base no tipo escolhido"""
        if self.balance <= self.stop_loss:
            print("Stop Loss atingido, encerrando operações.")
            return
        elif self.balance >= self.take_profit:
            print("Take Profit atingido, encerrando operações.")
            return

        if self.strategy_type == "basic":
            self.basic_strategy()
        elif self.strategy_type == "advanced":
            self.advanced_strategy()
        else:
            print("Estratégia desconhecida.")

    def generate_signal(self):
        """Gera sinal aleatório de compra ou venda"""
        return 'BUY' if random.choice([True, False]) else 'SELL'

    def basic_strategy(self):
        """Estratégia básica de compra e venda"""
        signal = self.generate_signal()
        print(f"Executando operação com sinal: {signal}")

        if signal == 'BUY':
            self.buy(self.trade_size)
        elif signal == 'SELL':
            self.sell(self.trade_size)

    def advanced_strategy(self):
        """Estratégia avançada com Stop Loss, Take Profit e ajuste de tamanho de operação"""
        if self.balance <= self.stop_loss:
            print("Stop Loss atingido, encerrando operações.")
            return
        elif self.balance >= self.take_profit:
            print("Take Profit atingido, encerrando operações.")
            return

        self.trade_size = self.calculate_trade_size()

        num_contracts = 1 if self.balance < 1000 else 2  # Lógica de número de contratos com base no saldo

        for _ in range(num_contracts):
            signal = self.generate_signal()
            if signal == "BUY":
                self.buy(self.trade_size)
            else:
                self.sell(self.trade_size)

            # Ajuste a sequência de ganhos
            if self.balance > 1000:
                self.gain_streak += 1
            else:
                self.gain_streak = 0

    def calculate_trade_size(self):
        """Calcula o tamanho da operação com base na sequência de ganhos"""
        return self.trade_size + (self.gain_streak * 5)  # Ajuste do tamanho com base na sequência de ganhos

    def buy(self, trade_size):
        """Executa uma compra"""
        if self.balance >= trade_size:
            self.balance -= trade_size
            print(f"Compra de {trade_size} unidades. Saldo: {self.balance}")
            self.record_operation('BUY', trade_size)
        else:
            print(f"Saldo insuficiente para realizar a compra de {trade_size} unidades.")

    def sell(self, trade_size):
        """Executa uma venda"""
        self.balance += trade_size
        print(f"Venda de {trade_size} unidades. Saldo: {self.balance}")
        self.record_operation('SELL', trade_size)

    def record_operation(self, trade_type, trade_size):
        """Grava a operação no banco de dados"""
        db = SessionLocal()
        try:
            operation = Operation(
                bot_name="Bot19",  # Nome do bot
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
    # Estratégia básica de compra e venda
    bot_basic = Bot19(saldo_inicial=1000, trade_size=10, strategy_type="basic")
    bot_basic.run()

    print("\n---- Operações com Estratégia Avançada ----\n")

    # Estratégia avançada com Stop Loss, Take Profit e ajuste de tamanho de operação
    bot_advanced = Bot19(saldo_inicial=1000, trade_size=10, strategy_type="advanced", stop_loss=900, take_profit=1100)
    bot_advanced.run()


def execute():
    """
    Função para executar a estratégia do Bot 
    Cria uma instância do Bot e executa a função run() para realizar as operações de compra e venda.
    """
    bot = Bot19(saldo_inicial=1000, trade_size=10, strategy_type="basic")  # Corrigido para Bot19
    print("Bot Strategy Executando...")  # Exibe uma mensagem indicando que o bot foi iniciado
    bot.run()  # Chama o método run() que executa a lógica de trading (compra ou venda)
