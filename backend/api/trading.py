# backend/api/trading.py

# Importações necessárias
from flask import Flask, Blueprint, jsonify
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import models, db_setup
from typing import Generator, Optional  # Adicionando Optional para indicar que alguns parâmetros podem ser None

# Importação das Estratégias (de Bot1 a Bot20)
from backend.strategies.bot_strategy1 import Bot1
# from backend.strategies.bot_strategy2 import Bot2
# from backend.strategies.bot_strategy3 import Bot3
# from backend.strategies.bot_strategy4 import Bot4
# from backend.strategies.bot_strategy5 import Bot5
# from backend.strategies.bot_strategy6 import Bot6
# from backend.strategies.bot_strategy7 import Bot7
# from backend.strategies.bot_strategy8 import Bot8
# from backend.strategies.bot_strategy9 import Bot9
# from backend.strategies.bot_strategy10 import Bot10
# from backend.strategies.bot_strategy11 import Bot11
# from backend.strategies.bot_strategy12 import Bot12
# from backend.strategies.bot_strategy13 import Bot13
# from backend.strategies.bot_strategy14 import Bot14
# from backend.strategies.bot_strategy15 import Bot15
# from backend.strategies.bot_strategy16 import Bot16
# from backend.strategies.bot_strategy17 import Bot17
# from backend.strategies.bot_strategy18 import Bot18
# from backend.strategies.bot_strategy19 import Bot19
# from backend.strategies.bot_strategy20 import Bot20

# Configuração do Flask
app = Flask(__name__)
trading_bp = Blueprint('trading_bp', __name__)

# Configuração do FastAPI
fastapi_app = FastAPI()
trading_router = APIRouter()

# Função para configurar o banco de dados e fornecer a sessão
def get_db_session() -> Generator[Session, None, None]:
    db_session = db_setup.get_session()  # Função que retorna uma nova sessão do banco
    try:
        yield db_session  # Yield a sessão para ser utilizada nas rotas
    finally:
        db_session.close()  # Fechar a sessão quando não for mais necessária

# Inicialização dos Robôs
robos = {i: {"nome": f"Robo{i}", "ativo": False, "instancia": None} for i in range(1, 21)}

# Associando cada instância de robô ao dicionário
robos[1]["instancia"] = Bot1()
# Exemplo de outras estratégias
# robos[2]["instancia"] = Bot2()
# robos[3]["instancia"] = Bot3()
# ...

# Função para executar o robô
def executar_robo(robo_id: int):
    robo = robos.get(robo_id)
    if robo and robo["ativo"]:
        instancia = robo["instancia"]
        instancia.run()  # Correção: A função run() deve ser chamada aqui
        return f"Robo {robo['nome']} executado com sucesso."
    return f"Robo {robo_id} não está ativo ou não existe."

# Função para interagir com o banco de dados e obter informações sobre os robôs
def get_robos_from_db(db_session: Session):
    robos_db = db_session.query(models.Robo).all()  # Exemplo de consulta
    return robos_db

# Rotas do Flask com Blueprint
@trading_bp.route('/ligar', methods=['POST'])
def ligar_robo(robo_id: Optional[int] = None):
    """Rota para ligar um robô específico. Agora aceita um robo_id opcional."""
    if robo_id is None:
        return jsonify({"message": "ID do robô é necessário."}), 400
    if robo_id in robos:  # Verifica se o robô existe
        if robos[robo_id]["ativo"]:  # Se o robô já estiver ativo
            return jsonify({"message": f"Robo {robos[robo_id]['nome']} já está ligado.", "status": "ativo"}), 200
        robos[robo_id]["ativo"] = True  # Ativa o robô
        return jsonify({"message": f"Robo {robos[robo_id]['nome']} ligado com sucesso.", "status": "ativo"}), 200
    return jsonify({"message": "Robo não encontrado.", "status": "erro"}), 404

@trading_bp.route('/desligar/<int:robo_id>', methods=['POST'])
def desligar_robo(robo_id):
    if robo_id in robos:
        if not robos[robo_id]["ativo"]:
            return jsonify({"message": f"Robo {robos[robo_id]['nome']} já está desligado.", "status": "inativo"}), 200
        robos[robo_id]["ativo"] = False
        return jsonify({"message": f"Robo {robos[robo_id]['nome']} desligado com sucesso.", "status": "inativo"}), 200
    return jsonify({"message": "Robo não encontrado.", "status": "erro"}), 404

@trading_bp.route('/listagem', methods=['GET'])
def listar_robos():
    lista_robos = [{"id": robo_id, "nome": dados["nome"], "ativo": dados["ativo"]} for robo_id, dados in robos.items()]
    return jsonify(lista_robos), 200

@trading_bp.route('/executar/<int:robo_id>', methods=['POST'])
def executar(robo_id):
    mensagem = executar_robo(robo_id)
    return jsonify({"message": mensagem}), 200 if "sucesso" in mensagem else 404

# Rotas FastAPI com a injeção de dependência para a sessão de banco de dados

@trading_router.get("/robots")
async def listar_robos_fastapi(db_session: Session = Depends(get_db_session)):
    """Rota FastAPI para listar robôs do banco de dados"""
    robos_db = get_robos_from_db(db_session)
    return [{"id": robo.id, "nome": robo.nome, "ativo": robo.ativo} for robo in robos_db]

@trading_router.post("/robots/{robo_id}/ligar")
async def ligar_robo_fastapi(robo_id: int, db_session: Session = Depends(get_db_session)):
    """Rota FastAPI para ligar um robô específico"""
    if robo_id in robos:
        if robos[robo_id]["ativo"]:
            return {"message": f"Robo {robos[robo_id]['nome']} já está ligado.", "status": "ativo"}
        robos[robo_id]["ativo"] = True
        return {"message": f"Robo {robos[robo_id]['nome']} ligado com sucesso.", "status": "ativo"}
    raise HTTPException(status_code=404, detail="Robo não encontrado.")

@trading_router.post("/robots/{robo_id}/desligar")
async def desligar_robo_fastapi(robo_id: int, db_session: Session = Depends(get_db_session)):
    """Rota FastAPI para desligar um robô específico"""
    if robo_id in robos:
        if not robos[robo_id]["ativo"]:
            return {"message": f"Robo {robos[robo_id]['nome']} já está desligado.", "status": "inativo"}
        robos[robo_id]["ativo"] = False
        return {"message": f"Robo {robos[robo_id]['nome']} desligado com sucesso.", "status": "inativo"}
    raise HTTPException(status_code=404, detail="Robo não encontrado.")

@trading_router.post("/robots/{robo_id}/executar")
async def executar_robo_fastapi(robo_id: int, db_session: Session = Depends(get_db_session)):
    """Rota FastAPI para executar um robô específico"""
    mensagem = executar_robo(robo_id)
    if "sucesso" in mensagem:
        return {"message": mensagem}
    raise HTTPException(status_code=404, detail=mensagem)

# Integração do Flask com FastAPI
@app.route('/')
def hello_world():
    return "Hello from Flask!"

# Registra o Blueprint no Flask
app.register_blueprint(trading_bp, url_prefix="/flask")

# Inclui as rotas FastAPI no FastAPI App
fastapi_app.include_router(trading_router, prefix="/fastapi", tags=["Robots"])

# Rodando o servidor Flask e FastAPI juntos (por exemplo com Uvicorn)
if __name__ == "__main__":
    from uvicorn import run
    from multiprocessing import Process

    def run_flask():
        app.run(debug=True, use_reloader=False)

    def run_fastapi():
        run(fastapi_app, host="0.0.0.0", port=8000)

    # Inicia Flask e FastAPI simultaneamente
    p1 = Process(target=run_flask)
    p2 = Process(target=run_fastapi)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
