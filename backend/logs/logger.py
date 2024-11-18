# backend/logs/logger.py
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO, max_size=5*1024*1024, backup_count=3):
    """
    Configura um logger que envia logs para um arquivo e opcionalmente para o console.
    
    :param name: Nome do logger.
    :param log_file: Caminho do arquivo de log.
    :param level: Nível de log (default é INFO).
    :param max_size: Tamanho máximo do arquivo de log antes de rotacionar (default é 5MB).
    :param backup_count: Número de arquivos antigos a manter durante a rotação de logs (default é 3).
    :return: O logger configurado.
    """
    # Criação do diretório de logs caso não exista
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Criar o manipulador para o arquivo de log com rotação
    file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
    file_handler.setLevel(level)
    
    # Criar o manipulador para o console (opcional)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    
    # Definir a formatação para os logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # Configurar o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

# Exemplo de uso
bot_logger = setup_logger('bot_logger', 'backend/logs/bot.log')

# Testando os logs
bot_logger.info('Logger de Bot iniciado com sucesso.')
bot_logger.warning('Este é um aviso de teste.')
bot_logger.error('Este é um erro de teste.')
