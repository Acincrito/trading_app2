# backend/database/db_setup.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./trader_app.db"  # Pode substituir por outro banco de dados, como PostgreSQL ou MySQL

# Criando o engine para conectar ao banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criando a classe base para os modelos
Base = declarative_base()

# Criando o session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definindo o modelo de dados Robot (robô)
class RobotModel(Base):
    __tablename__ = "robots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    strategy = Column(String)
    balance = Column(Float)

# Definindo o modelo de entrada para leitura (usado em Pydantic)
class Robot(BaseModel):
    id: int
    name: str
    strategy: str
    balance: float

    class Config:
        orm_mode = True  # Permite que o Pydantic entenda o modelo SQLAlchemy

# Função de dependência para obter a sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db  # Retorna a sessão para ser usada no endpoint
    finally:
        db.close()  # Garante que a sessão seja fechada após o uso

# Inicializando o FastAPI
app = FastAPI()

# Endpoint para obter todos os robôs
@app.get("/robots/", response_model=List[Robot])
def read_robots(db: Session = Depends(get_db)):
    robots = db.query(RobotModel).all()
    return robots  # FastAPI fará a conversão automaticamente para o modelo Pydantic

# Endpoint para criar um novo robô
@app.post("/robots/", response_model=Robot)
def create_robot(robot: Robot, db: Session = Depends(get_db)):
    db_robot = RobotModel(name=robot.name, strategy=robot.strategy, balance=robot.balance)
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)  # Atualiza a instância com os dados do banco de dados
    return db_robot

# Endpoint para obter um robô específico pelo ID
@app.get("/robots/{robot_id}", response_model=Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    db_robot = db.query(RobotModel).filter(RobotModel.id == robot_id).first()
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return db_robot
