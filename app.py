# app.py
import multiprocessing
from backend.create_app import create_app
from backend.strategies import (
    bot_strategy1, #bot_strategy2, bot_strategy3, bot_strategy4, bot_strategy5,
    #bot_strategy6, bot_strategy7, bot_strategy8, bot_strategy9, bot_strategy10,
    #bot_strategy11, bot_strategy12, bot_strategy13, bot_strategy14, bot_strategy15,
    #bot_strategy16, bot_strategy17, bot_strategy18, bot_strategy19, bot_strategy20
)  # Adicione todos os bots necessários
from config import Config
from fastapi import FastAPI
from backend.api.trading import trading_router  # Este import deve ser usado para configurar as rotas
from waitress import serve

def run_bot(bot_function):
    """Executa o bot passado como argumento."""
    print(f"Iniciando {bot_function.__name__}...")
    bot_function()  # Chama a função de execução do bot
    print(f"{bot_function.__name__} finalizado.")

def start_server():
    """Função que inicializa o servidor FastAPI com Waitress."""
    # Criando a aplicação FastAPI diretamente
    app = FastAPI()

    # Criação da aplicação FastAPI usando configuração
    create_app(Config)

    # Adicionando o trading_router à aplicação
    app.include_router(trading_router)  # Agora o router será utilizado

    # Iniciando o servidor usando Waitress
    print("Iniciando o servidor...")
    serve(app, host='0.0.0.0', port=5001)
    print("Servidor iniciado.")

def start_bots():
    """Função para iniciar os bots em processos paralelos."""
    # Lista de bots a serem executados
    bot_functions = [
        bot_strategy1.execute,# bot_strategy2.execute, bot_strategy3.execute, bot_strategy4.execute,
        #bot_strategy5.execute, bot_strategy6.execute, bot_strategy7.execute, bot_strategy8.execute,
        #bot_strategy9.execute, bot_strategy10.execute, bot_strategy11.execute, bot_strategy12.execute,
        #bot_strategy13.execute, bot_strategy14.execute, bot_strategy15.execute, bot_strategy16.execute,
        #bot_strategy17.execute, bot_strategy18.execute, bot_strategy19.execute, bot_strategy20.execute
    ]
    
    # Executando os bots em processos paralelos
    print("Iniciando os bots...")
    bot_processes = []
    for bot_function in bot_functions:
        process = multiprocessing.Process(target=run_bot, args=(bot_function,))
        process.start()
        bot_processes.append(process)

    # Aguardar a conclusão dos bots
    for process in bot_processes:
        process.join()
    print("Todos os bots finalizaram.")

if __name__ == "__main__":
    # Rodando o servidor e bots em processos paralelos
    print("Iniciando processo principal...")

    # Processo para rodar o servidor
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()

    # Processo para rodar os bots
    bot_process = multiprocessing.Process(target=start_bots)
    bot_process.start()

    # Aguardar ambos os processos
    server_process.join()
    bot_process.join()

    print("Processos concluídos.")
