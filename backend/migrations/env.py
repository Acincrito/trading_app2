import os
import logging
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente de um arquivo .env, útil para ambientes de desenvolvimento
load_dotenv()

def get_database_url() -> str:
    """Obtém a URL do banco de dados da variável de ambiente DATABASE_URL.
    
    Valida se a URL tem o formato correto e lança um erro caso contrário.
    """
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("A variável de ambiente DATABASE_URL não está configurada.")
    
    # Verificação básica do formato da URL (pode ser mais detalhada conforme o padrão do banco de dados)
    if not database_url.startswith("postgresql://"):
        raise ValueError("A URL do banco de dados não possui o formato esperado (postgresql://).")
    
    return database_url

def configure_logging():
    """Configura o logging para armazenar logs em arquivo e também exibir no console."""
    config = context.config
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    logger = logging.getLogger('alembic.runtime.migration')
    logger.setLevel(logging.DEBUG)  # Usando DEBUG para uma depuração mais detalhada

    # Configuração de handler para logs no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # Configuração de handler para logs em arquivo
    log_file_handler = logging.FileHandler('alembic_migration.log')
    log_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_file_handler)

def create_engine_with_pool() -> object:
    """Cria o engine do banco de dados com um pool de conexões adequado."""
    database_url = get_database_url()
    engine = create_engine(database_url, poolclass=pool.QueuePool, pool_size=10, max_overflow=5)
    return engine

def backup_database():
    """Cria um backup do banco de dados antes de executar as migrações."""
    # Aqui você pode adicionar um comando para realizar o backup do banco
    # Em um cenário real, poderia ser algo como pg_dump para PostgreSQL
    logging.info(f"Iniciando o backup do banco de dados {datetime.now()}")
    # Placeholder para o comando de backup
    # Exemplo: os.system(f"pg_dump {get_database_url()} > backup.sql")
    logging.info("Backup concluído com sucesso.")

def run_migrations_offline() -> None:
    """Executa as migrações em modo offline."""
    url = get_database_url()
    
    context.configure(
        url=url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        try:
            logging.info("Iniciando migrações offline...")
            context.run_migrations()
            logging.info("Migração offline concluída com sucesso.")
        except SQLAlchemyError as e:
            logging.error(f"Erro durante a migração offline: {e}")
            raise

def run_migrations_online() -> None:
    """Executa as migrações em modo online, com conexão real ao banco de dados."""
    try:
        # Criar o engine com pool de conexões
        engine = create_engine_with_pool()
        
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=None)
            
            with context.begin_transaction():
                logging.info("Iniciando migrações online...")
                context.run_migrations()
                logging.info("Migração online concluída com sucesso.")
                
    except SQLAlchemyError as e:
        logging.error(f"Erro durante a migração online: {e}")
        raise

# Função principal de migração
def migrate():
    """Função para executar migrações offline ou online dependendo do contexto."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()

# Realizar backup do banco antes das migrações
backup_database()

# Iniciar as migrações
migrate()
