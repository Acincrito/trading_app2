# /backend/trader_app/data_handler.py

import json
import os
import logging
import shutil

# Configurações de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path="data.json"):
    """
    Carrega os dados dos robôs e histórico a partir de um arquivo JSON.

    Parameters:
        file_path (str): Caminho para o arquivo JSON a ser carregado. O padrão é "data.json".

    Returns:
        tuple: Um tupla contendo dois elementos:
            - Um dicionário com os dados dos robôs.
            - Uma lista com o histórico de operações.
    """
    if not os.path.exists(file_path):
        logging.warning(f"Arquivo {file_path} não encontrado. Retornando dados vazios.")
        return {}, []  # Retorna valores padrão caso o arquivo não exista

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            robots = data.get("robots", {})
            history = data.get("history", [])
            
            # Validar se 'robots' é um dicionário e 'history' é uma lista
            if not isinstance(robots, dict) or not isinstance(history, list):
                raise ValueError("Formato de dados inválido no arquivo.")
            logging.info(f"Dados carregados com sucesso de {file_path}")
            return robots, history
    except (json.JSONDecodeError, ValueError) as e:
        # Captura erros de leitura e formatação JSON
        logging.error(f"Erro ao carregar dados de {file_path}: {e}")
        return {}, []  # Retorna valores padrão em caso de erro

def save_data(robots, history, file_path="data.json", backup=True):
    """
    Salva os dados dos robôs e histórico em um arquivo JSON.

    Parameters:
        robots (dict): Dados dos robôs a serem salvos.
        history (list): Histórico de operações a ser salvo.
        file_path (str): Caminho para o arquivo onde os dados serão salvos. O padrão é "data.json".
        backup (bool): Se True, cria um backup do arquivo antes de salvar os novos dados. O padrão é True.
    """
    # Validar se 'robots' é um dicionário e 'history' é uma lista antes de salvar
    if not isinstance(robots, dict) or not isinstance(history, list):
        logging.error("Erro: 'robots' deve ser um dicionário e 'history' deve ser uma lista.")
        return

    # Criar backup antes de sobrescrever o arquivo
    if backup and os.path.exists(file_path):
        backup_path = file_path + ".bak"
        try:
            shutil.copy(file_path, backup_path)  # Cria uma cópia de segurança
            logging.info(f"Backup do arquivo criado em {backup_path}")
        except IOError as e:
            logging.error(f"Erro ao criar backup de {file_path}: {e}")
            return

    try:
        with open(file_path, "w") as f:
            json.dump({"robots": robots, "history": history}, f, indent=4)
            logging.info(f"Dados salvos com sucesso em {file_path}")
    except IOError as e:
        logging.error(f"Erro ao salvar dados em {file_path}: {e}")

# Exemplo de uso
if __name__ == "__main__":
    robots, history = load_data()

    # Modificar os dados (simulação)
    robots["robot1"] = {"status": "on", "trade_count": 10}
    history.append({"action": "buy", "symbol": "BTCUSD", "amount": 100})

    save_data(robots, history)
