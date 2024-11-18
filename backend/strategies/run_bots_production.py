import pytest
from backend.strategies.bot_strategy1 import Bot1
from backend.strategies.bot_strategy2 import Bot2
from backend.strategies.bot_strategy3 import Bot3
from backend.strategies.bot_strategy4 import Bot4
from backend.strategies.bot_strategy5 import Bot5
from backend.strategies.bot_strategy6 import Bot6
from backend.strategies.bot_strategy7 import Bot7
from backend.strategies.bot_strategy8 import Bot8
from backend.strategies.bot_strategy9 import Bot9
from backend.strategies.bot_strategy10 import Bot10
from backend.strategies.bot_strategy11 import Bot11
from backend.strategies.bot_strategy12 import Bot12
from backend.strategies.bot_strategy13 import Bot13
from backend.strategies.bot_strategy14 import Bot14
from backend.strategies.bot_strategy15 import Bot15
from backend.strategies.bot_strategy16 import Bot16
from backend.strategies.bot_strategy17 import Bot17
from backend.strategies.bot_strategy18 import Bot18
from backend.strategies.bot_strategy19 import Bot19
from backend.strategies.bot_strategy20 import Bot20

# Lista de classes de bots
bot_classes = [
    Bot1, Bot2, Bot3, Bot4, Bot5, 
    Bot6, Bot7, Bot8, Bot9, Bot10, 
    Bot11, Bot12, Bot13, Bot14, Bot15, 
    Bot16, Bot17, Bot18, Bot19, Bot20
]

@pytest.mark.parametrize("bot_class", bot_classes)
def test_bot_strategy_execution(bot_class):
    """Testando a execução de todos os bots e garantindo que o saldo seja atualizado corretamente."""
    bot = bot_class(bot_name=bot_class.__name__)  # Instanciando dinamicamente o bot com o nome da classe
    print(f"Executando {bot.bot_name}...")
    
    # Inicializa e executa o bot
    bot.run()

    # Verifica se o saldo foi atualizado corretamente
    assert bot.balance != 1000, f"Falha na execução de {bot.bot_name}. O saldo não foi atualizado corretamente."

    print(f"Saldo atual de {bot.bot_name}: {bot.balance}")

def test_multiple_bots_execution():
    """Testando a execução de múltiplos bots de forma sequencial."""
    bots = [bot_class(bot_name=bot_class.__name__) for bot_class in bot_classes]
    
    for bot in bots:
        print(f"Executando {bot.bot_name}...")
        bot.run()
        assert bot.balance != 1000, f"Falha na execução de {bot.bot_name}. O saldo não foi atualizado corretamente."
        print(f"Saldo atual de {bot.bot_name}: {bot.balance}")
