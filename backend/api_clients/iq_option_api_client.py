# /backend/api_clients/iq_option_api_client.py

import logging
from iqoptionapi.stable_api import IQ_Option
import requests
from typing import Dict, Any


# Configuração do logger
def setup_logger() -> logging.Logger:
    logger = logging.getLogger('IQOptionBot')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

# Funções auxiliares para validações
def validate_symbol(symbol: str) -> bool:
    """Valida se o símbolo de negociação é válido (exemplo simplificado)."""
    valid_symbols = ["EURUSD", "GBPUSD", "BTCUSD"]
    return symbol in valid_symbols

def validate_action(action: str) -> bool:
    """Valida se a ação (compra ou venda) é válida."""
    return action.lower() in ["buy", "sell"]

def validate_amount(amount: float) -> bool:
    """Valida se o valor da transação é positivo."""
    return amount > 0

class IQOptionBase:
    """Classe base comum para interagir com a IQ Option, seja via WebSocket ou HTTP."""

    def __init__(self, username: str, password: str):
        """Inicializa o cliente com as credenciais de login."""
        self.username = username
        self.password = password
        self.logger = setup_logger()

    def login(self) -> Dict[str, Any]:
        """Método de login genérico que será sobrescrito nas subclasses."""
        raise NotImplementedError

    def execute_trade(self, symbol: str, action: str, amount: float) -> Dict[str, Any]:
        """Método de execução de trade genérico que será sobrescrito nas subclasses."""
        raise NotImplementedError

    def check_balance(self) -> Dict[str, Any]:
        """Método de verificação de saldo genérico que será sobrescrito nas subclasses."""
        raise NotImplementedError


class IQOptionBot(IQOptionBase):
    """Implementação do IQOptionBot usando a biblioteca iqoptionapi (WebSocket)."""

    def __init__(self, email: str, password: str):
        """Inicializa o bot com o email e senha para autenticação."""
        super().__init__(email, password)
        self.api = IQ_Option(email, password)
        self.api.connect()
        self.logger.info(f"Conectado ao IQ Option com {email}")

    def login(self) -> Dict[str, Any]:
        """Realiza o login via WebSocket."""
        return {"status": "success", "message": "Conectado ao IQ Option via WebSocket"}

    def execute_trade(self, symbol: str, action: str, amount: float) -> Dict[str, Any]:
        """Executa uma ordem de compra ou venda via WebSocket."""
        # Validando parâmetros
        if not validate_symbol(symbol):
            self.logger.error(f"Símbolo inválido: {symbol}")
            return {"status": "error", "message": "Símbolo inválido"}
        
        if not validate_action(action):
            self.logger.error(f"Ação inválida: {action}")
            return {"status": "error", "message": "Ação inválida"}
        
        if not validate_amount(amount):
            self.logger.error(f"Quantidade inválida: {amount}")
            return {"status": "error", "message": "Quantidade inválida"}
        
        # Executando trade
        try:
            direction = 'call' if action.lower() == 'buy' else 'put'
            success, order = self.api.buy(amount, symbol, direction, 1)
            if success:
                self.logger.info(f"Ordem executada: {action} {symbol} com valor {amount}")
                return {"status": "success", "order": order}
            else:
                return {"status": "error", "message": "Falha ao executar ordem."}
        except Exception as e:
            self.logger.error(f"Erro ao executar trade: {str(e)}")
            return {"status": "error", "message": str(e)}

    def check_balance(self) -> Dict[str, Any]:
        """Retorna o saldo atual da conta via WebSocket."""
        try:
            balance = self.api.get_balance()
            self.logger.info(f"Saldo atual: {balance}")
            return {"status": "success", "balance": balance}
        except Exception as e:
            self.logger.error(f"Erro ao verificar saldo: {str(e)}")
            return {"status": "error", "message": str(e)}


class IQOptionAPIClient(IQOptionBase):
    """Implementação do IQOptionBot usando a API HTTP (requests)."""

    def __init__(self, username: str, password: str):
        """Inicializa o cliente com o nome de usuário e senha para autenticação via API HTTP."""
        super().__init__(username, password)
        self.base_url = "https://iqoption.com/api"
        self.session = requests.Session()  # Reutilizar sessão HTTP

    def login(self) -> Dict[str, Any]:
        """Realiza o login via API HTTP."""
        try:
            response = self.session.post(f"{self.base_url}/login", data={"username": self.username, "password": self.password})
            if response.status_code == 200:
                self.logger.info("Login bem-sucedido via API HTTP.")
                return {"status": "success", "message": "Conectado ao IQ Option via API HTTP"}
            else:
                self.logger.error(f"Falha no login: {response.text}")
                return {"status": "error", "message": response.text}
        except requests.RequestException as e:
            self.logger.error(f"Erro ao tentar fazer login: {str(e)}")
            return {"status": "error", "message": str(e)}

    def execute_trade(self, symbol: str, action: str, amount: float) -> Dict[str, Any]:
        """Executa uma operação de compra ou venda via API HTTP."""
        # Validando parâmetros
        if not validate_symbol(symbol):
            self.logger.error(f"Símbolo inválido: {symbol}")
            return {"status": "error", "message": "Símbolo inválido"}
        
        if not validate_action(action):
            self.logger.error(f"Ação inválida: {action}")
            return {"status": "error", "message": "Ação inválida"}
        
        if not validate_amount(amount):
            self.logger.error(f"Quantidade inválida: {amount}")
            return {"status": "error", "message": "Quantidade inválida"}
        
        # Executando trade
        try:
            response = self.session.post(f"{self.base_url}/trade", json={
                "symbol": symbol,
                "action": action,  # 'buy' ou 'sell'
                "amount": amount
            })
            if response.status_code == 200:
                return {"status": "success", "order": response.json()}
            else:
                return {"status": "error", "message": response.text}
        except requests.RequestException as e:
            self.logger.error(f"Erro ao executar trade via API HTTP: {str(e)}")
            return {"status": "error", "message": str(e)}

    def check_balance(self) -> Dict[str, Any]:
        """Retorna o saldo atual da conta via API HTTP."""
        try:
            response = self.session.get(f"{self.base_url}/balance", params={"username": self.username})
            if response.status_code == 200:
                return {"status": "success", "balance": response.json()}
            else:
                return {"status": "error", "message": response.text}
        except requests.RequestException as e:
            self.logger.error(f"Erro ao verificar saldo via API HTTP: {str(e)}")
            return {"status": "error", "message": str(e)}
