# Importando os módulos necessários do SQLAlchemy
# backend/database/models.py
# Importando os módulos necessários do SQLAlchemy
import enum
import time
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from cryptography.fernet import Fernet
from loguru import logger
import schedule
from databases import Database
from typing import Optional  # Corrigido: Importando Optional

# Configuração do banco de dados PostgreSQL com databases (assíncrono)
DATABASE_URL = "postgresql://username:password@localhost/mydatabase"
db = Database(DATABASE_URL)

# Definindo os Enums para o Status do Robô e Tipo de Operação
class RobotStatus(enum.Enum):
    ON = "ON"
    OFF = "OFF"

class TradeType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

# Função para obter o timestamp atual
def get_current_timestamp():
    return pd.Timestamp.now()  # Retorna um objeto Timestamp do Pandas, que é aceito pelo PostgreSQL

# Definindo as tabelas com comandos SQL
ROBOT_TABLE = """
CREATE TABLE IF NOT EXISTS robots (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    strategy VARCHAR NOT NULL,
    balance FLOAT DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"""

OPERATION_TABLE = """
CREATE TABLE IF NOT EXISTS operations (
    id SERIAL PRIMARY KEY,
    bot_name VARCHAR NOT NULL,
    trade_type VARCHAR NOT NULL,
    amount FLOAT NOT NULL,
    signal VARCHAR NOT NULL,
    balance_after FLOAT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    robot_id INTEGER REFERENCES robots(id)
);
"""

# Classe Operation para representar a operação
class Operation(BaseModel):
    bot_name: str
    robot_id: int  # Deve ser um número inteiro
    signal: str
    amount: float
    balance_after: float
    timestamp: str
    id: Optional[int] = None  # Caso o id seja gerado automaticamente pelo banco


# Função assíncrona para gravar a operação no banco de dados
async def record_operation(trade_type, trade_size, robot_id, bot_name, signal, balance_after):
    try:
        query = """
        INSERT INTO operations (bot_name, trade_type, amount, signal, balance_after, robot_id)
        VALUES (:bot_name, :trade_type, :amount, :signal, :balance_after, :robot_id)
        RETURNING id, bot_name, trade_type, amount, signal, balance_after, timestamp, robot_id
        """
        operation = await db.fetch_one(query, values={
            "bot_name": bot_name,
            "trade_type": trade_type,
            "amount": trade_size,
            "signal": signal,
            "balance_after": balance_after,
            "robot_id": robot_id
        })
        if operation:
            logger.info(f"Operação registrada com sucesso: {operation}")
            return Operation(**operation)  # Retorna o objeto Operation com os dados da operação
    except Exception as e:
        logger.error(f"Erro ao gravar a operação no banco de dados: {e}")
        return None  # Retorna None em caso de erro

# Função assíncrona para realizar uma operação e ajustar o saldo
async def perform_trade(robot_id, trade_type, trade_size, bot_name, signal):
    async with db.transaction():
        query = "SELECT * FROM robots WHERE id = :robot_id"
        robot = await db.fetch_one(query, values={"robot_id": robot_id})

        if robot:
            balance_after = robot["balance"]
            if trade_type == TradeType.BUY:
                if robot["balance"] >= trade_size:
                    # Subtrai saldo para uma operação de compra
                    update_query = "UPDATE robots SET balance = balance - :trade_size WHERE id = :robot_id"
                    await db.execute(update_query, values={"trade_size": trade_size, "robot_id": robot_id})
                    balance_after -= trade_size
                else:
                    logger.warning(f"Saldo insuficiente para {trade_type} no robô {robot['name']}")
                    return None
            elif trade_type == TradeType.SELL:
                # Adiciona saldo para uma operação de venda
                update_query = "UPDATE robots SET balance = balance + :trade_size WHERE id = :robot_id"
                await db.execute(update_query, values={"trade_size": trade_size, "robot_id": robot_id})
                balance_after += trade_size
            
            # Registra a operação no histórico e retorna um objeto Operation
            operation = await record_operation(trade_type, trade_size, robot_id, bot_name, signal, balance_after)
            return operation
        else:
            logger.error(f"Robô com ID {robot_id} não encontrado.")
            return None

# Função assíncrona para visualizar o histórico de operações com pandas
async def get_operations_history():
    query = "SELECT * FROM operations ORDER BY timestamp DESC"
    operations = await db.fetch_all(query)
    data = [
        {
            "Operation ID": op["id"],
            "Bot Name": op["bot_name"],
            "Trade Type": op["trade_type"],
            "Amount": op["amount"],
            "Signal": op["signal"],
            "Balance After": op["balance_after"],
            "Timestamp": op["timestamp"]
        }
        for op in operations
    ]
    
    # Criando um DataFrame com o histórico de operações
    df = pd.DataFrame(data)
    
    # Exibindo o DataFrame no console
    logger.info(f"Histórico de operações:\n{df}")
    
    # Retornando o DataFrame
    return df

# Função para criptografar dados sensíveis
def encrypt_data(data: str, key: bytes) -> str:
    cipher = Fernet(key)
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

# Função para gerar uma chave para criptografia
def generate_key() -> bytes:
    return Fernet.generate_key()

# Função para inicializar o banco de dados (assíncrono)
async def init_db():
    await db.connect()
    # Criando as tabelas
    await db.execute(ROBOT_TABLE)
    await db.execute(OPERATION_TABLE)
    await db.disconnect()

# Função para agendar tarefas
def job():
    logger.info("Agendando operação de rotina...")

# Criando o servidor FastAPI para controle de robôs via web
app = FastAPI()

class RobotCreate(BaseModel):
    name: str
    strategy: str
    balance: float

@app.post("/robots/")
async def create_robot(robot: RobotCreate):
    await db.connect()
    query = """
    INSERT INTO robots (name, strategy, balance)
    VALUES (:name, :strategy, :balance)
    RETURNING id, name, strategy, balance, created_at, updated_at
    """
    new_robot = await db.fetch_one(query, values={"name": robot.name, "strategy": robot.strategy, "balance": robot.balance})
    await db.disconnect()
    return new_robot

@app.get("/operations/")  
async def get_operations():
    return await get_operations_history()

# Função principal assíncrona
async def main():
    # Gerar chave para criptografia
    key = generate_key()
    encrypted_data = encrypt_data("Sensitive Data", key)
    logger.info(f"Dados criptografados: {encrypted_data}")

    # Inicializar o banco de dados
    await init_db()

    # Realizando uma operação de compra (BUY)
    operation = await perform_trade(robot_id=1, trade_type=TradeType.BUY, trade_size=10.0, bot_name="Bot1", signal="BUY_SIGNAL")
    if operation:
        logger.info(f"Operação realizada: {operation}")
    
    # Realizando uma operação de venda (SELL)
    operation = await perform_trade(robot_id=1, trade_type=TradeType.SELL, trade_size=5.0, bot_name="Bot1", signal="SELL_SIGNAL")
    if operation:
        logger.info(f"Operação realizada: {operation}")
    
    # Exibindo o histórico de operações com pandas
    await get_operations_history()

# Função para rodar o agendador
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Executando as tarefas agendadas e o código principal de forma assíncrona
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Iniciando a execução assíncrona do código

    # Rodando o agendador em um thread separado
    from threading import Thread
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

    # Aguardando o término do código principal
    loop.run_forever()
