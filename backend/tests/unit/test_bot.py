# backend/tests/unit/test_bot.py
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

# Parametrizando as classes de bots para os testes
@pytest.mark.parametrize("bot_strategy_class", [
    Bot1, Bot2, Bot3, Bot4, Bot5, Bot6, Bot7, Bot8, Bot9, Bot10,
    Bot11, Bot12, Bot13, Bot14, Bot15, Bot16, Bot17, Bot18, Bot19, Bot20
])
@pytest.fixture
def bot_strategy(bot_strategy_class):
    """Fixture para criar a instância do bot_strategy."""
    return bot_strategy_class()

def test_initialization(bot_strategy):
    """Testando a inicialização do saldo e do tamanho da operação para todos os bots."""
    assert bot_strategy.balance == 1000, f"Falha na inicialização do saldo para {bot_strategy.__class__.__name__}, saldo esperado: 1000, saldo atual: {bot_strategy.balance}"
    assert bot_strategy.trade_size == 10, f"Falha na inicialização do tamanho da operação para {bot_strategy.__class__.__name__}, tamanho esperado: 10, tamanho atual: {bot_strategy.trade_size}"

def test_buy_sell_operations(bot_strategy):
    """Testando a operação de compra e venda para todos os bots."""
    initial_balance = bot_strategy.balance
    
    # Realizando uma compra
    bot_strategy.buy()
    expected_balance_after_buy = initial_balance - bot_strategy.trade_size
    assert bot_strategy.balance == expected_balance_after_buy, (
        f"Falha no teste de compra para {bot_strategy.__class__.__name__}. "
        f"Saldo esperado após compra: {expected_balance_after_buy}, saldo atual: {bot_strategy.balance}"
    )
    
    # Realizando uma venda
    bot_strategy.sell()
    assert bot_strategy.balance == initial_balance, (
        f"Falha no teste de venda para {bot_strategy.__class__.__name__}. "
        f"Saldo esperado após venda: {initial_balance}, saldo atual: {bot_strategy.balance}"
    )

def test_buy_sell(bot_strategy):
    """Testando a compra e venda para garantir que o saldo seja ajustado corretamente."""
    initial_balance = bot_strategy.balance  # Saldo inicial do bot_strategy
    
    # Testando compra
    bot_strategy.buy()  # O bot_strategy faz uma compra
    expected_balance_after_buy = initial_balance - bot_strategy.trade_size
    assert bot_strategy.balance == expected_balance_after_buy, (
        f"Falha no teste de compra para {bot_strategy.__class__.__name__}. "
        f"Saldo esperado: {expected_balance_after_buy}, saldo atual: {bot_strategy.balance}"
    )

    # Testando venda
    bot_strategy.sell()  # O bot_strategy faz uma venda
    assert bot_strategy.balance == initial_balance, (
        f"Falha no teste de venda para {bot_strategy.__class__.__name__}. "
        f"Saldo esperado: {initial_balance}, saldo atual: {bot_strategy.balance}"
    )

def test_generate_signal(bot_strategy):
    """Testando a geração de sinal (BUY ou SELL) para todos os bots."""
    signal = bot_strategy.generate_signal()  # Gerando um sinal
    assert signal in ['BUY', 'SELL'], (
        f"Falha na geração de sinal para {bot_strategy.__class__.__name__}. "
        f"Sinal gerado: {signal}. Esperado 'BUY' ou 'SELL'."
    )

def test_balance_limits(bot_strategy):
    """Testando limites do saldo para garantir que não ultrapasse o saldo inicial ou que o saldo não fique negativo."""
    initial_balance = bot_strategy.balance

    # Tentando fazer uma operação maior que o saldo
    bot_strategy.balance = 5  # Definindo um saldo baixo para o teste
    bot_strategy.buy()
    assert bot_strategy.balance >= 0, (
        f"Falha na verificação de saldo negativo para {bot_strategy.__class__.__name__}. "
        f"Saldo esperado após compra não pode ser negativo. Saldo atual: {bot_strategy.balance}"
    )

    # Restaurando o saldo inicial para o teste
    bot_strategy.balance = initial_balance

def test_signal_accuracy(bot_strategy):
    """Verificando se os sinais gerados são válidos dentro do contexto de estratégia."""
    valid_signals = ['BUY', 'SELL']
    signal = bot_strategy.generate_signal()
    assert signal in valid_signals, (
        f"Falha na geração de sinal válido para {bot_strategy.__class__.__name__}. "
        f"Sinal gerado: {signal}. Esperado: um dos sinais válidos {valid_signals}."
    )
