# backend/strategies/base_bot.py

import logging
from backend.database.models import Operation
from backend.database.db_setup import SessionLocal
from datetime import datetime
import random
from typing import Optional

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseBot:
    def __init__(self, bot_name: str, robot_id: int, balance: Optional[float] = 1000, trade_size: Optional[float] = 10):
        """Inicializa o bot com nome, ID, saldo inicial e tamanho da operação."""
        self.bot_name = bot_name
        self.robot_id = robot_id
        self.balance = balance
        self.trade_size = trade_size
        logging.info(f"{self.bot_name} iniciado com saldo inicial de {self.balance} e tamanho de operação de {self.trade_size}")

    def run(self):
        """Executa a estratégia de trading (compra ou venda)."""
        signal = self.generate_signal()
        logging.info(f"Gerando sinal de operação: {signal} para {self.bot_name}")
        if signal == 'BUY':
            self.buy()
        elif signal == 'SELL':
            self.sell()

    def generate_signal(self) -> str:
        """Gera um sinal aleatório de compra ou venda."""
        signal = 'BUY' if random.choice([True, False]) else 'SELL'
        return signal

    def buy(self):
        """Executa a operação de compra se houver saldo suficiente."""
        if self.balance >= self.trade_size:
            self.balance -= self.trade_size
            self.record_operation('BUY')
            logging.info(f"Compra realizada por {self.bot_name}. Novo saldo: {self.balance}")
        else:
            logging.warning(f"{self.bot_name} - Saldo insuficiente para compra. Saldo disponível: {self.balance}")

    def sell(self):
        """Executa a operação de venda e atualiza o saldo."""
        self.balance += self.trade_size
        self.record_operation('SELL')
        logging.info(f"Venda realizada por {self.bot_name}. Novo saldo: {self.balance}")

    def record_operation(self, trade_type: str):
        """Grava a operação de trading no banco de dados."""
        try:
            with SessionLocal() as db:
                operation = Operation(
                    bot_name=self.bot_name,
                    trade_type=trade_type,
                    amount=self.trade_size,
                    timestamp=datetime.now(),
                    robot_id=self.robot_id
                )
                db.add(operation)
                db.commit()
                logging.info(f"Operação {trade_type} registrada no banco para {self.bot_name}")
        except Exception as e:
            logging.error(f"Erro ao gravar operação no banco de dados: {e}")

    def get_balance(self) -> float:
        """Retorna o saldo atual do bot."""
        return self.balance

    def set_balance(self, balance: float):
        """Configura um novo saldo para o bot."""
        self.balance = balance
        logging.info(f"{self.bot_name} - Novo saldo definido: {self.balance}")

    def set_trade_size(self, trade_size: float):
        """Configura o novo tamanho de operação."""
        self.trade_size = trade_size
        logging.info(f"{self.bot_name} - Novo tamanho de operação definido: {self.trade_size}")
