import requests
from config import CONFIG

class TradingAPI:
    def __init__(self):
        # Configuração com URLs das corretoras
        self.broker_urls = CONFIG.get("broker_urls", {})
    
    def place_trade(self, broker, symbol, trade_type, amount):
        """
        Faz uma operação de compra ou venda em uma corretora específica.
        
        Args:
            broker (str): Nome da corretora.
            symbol (str): Símbolo do ativo (ex: BTC/USD).
            trade_type (str): Tipo de operação ("buy" ou "sell").
            amount (float): Quantidade da operação.

        Returns:
            dict: Resposta da corretora ou erro.
        """
        # Obtém a URL da corretora
        url = self.broker_urls.get(broker)
        if not url:
            return {"error": "Corretora não encontrada"}
        
        # Validação básica dos parâmetros
        if trade_type not in ["buy", "sell"]:
            return {"error": "Tipo de operação inválido. Use 'buy' ou 'sell'."}
        if amount <= 0:
            return {"error": "O valor da operação deve ser maior que zero."}
        
        # Envia a solicitação para a API da corretora
        try:
            response = requests.post(url, json={
                "symbol": symbol,
                "trade_type": trade_type,
                "amount": amount,
            })
            response.raise_for_status()  # Lança uma exceção para status de erro HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro ao conectar com a corretora: {e}"}

    def execute_strategy(self, strategy_name, parameters):
        """
        Executa uma estratégia de trading específica.

        Args:
            strategy_name (str): Nome da estratégia.
            parameters (dict): Parâmetros para a estratégia.

        Returns:
            dict: Resultado da estratégia ou erro.
        """
        if strategy_name == "simple_moving_average":
            return self._simple_moving_average(parameters)
        elif strategy_name == "breakout_strategy":
            return self._breakout_strategy(parameters)
        else:
            return {"error": f"Estratégia '{strategy_name}' não encontrada."}

    def _simple_moving_average(self, parameters):
        """
        Estratégia de média móvel simples (exemplo de implementação).

        Args:
            parameters (dict): Parâmetros da estratégia, incluindo:
                - 'symbol': Ativo a ser analisado.
                - 'period': Período da média móvel.
                - 'prices': Lista de preços para cálculo.

        Returns:
            dict: Resultado da estratégia.
        """
        symbol = parameters.get("symbol", "N/A")
        period = parameters.get("period", 14)  # Período padrão
        prices = parameters.get("prices", [])
        
        if len(prices) < period:
            return {"error": "Dados insuficientes para o cálculo da média móvel."}
        
        sma = sum(prices[-period:]) / period
        return {
            "status": "success",
            "symbol": symbol,
            "sma": sma,
            "details": f"Média móvel simples calculada com período {period}."
        }

    def _breakout_strategy(self, parameters):
        """
        Estratégia de breakout (exemplo de implementação).

        Args:
            parameters (dict): Parâmetros da estratégia, incluindo:
                - 'symbol': Ativo a ser analisado.
                - 'high': Máxima de preço.
                - 'low': Mínima de preço.
                - 'current_price': Preço atual.

        Returns:
            dict: Resultado da estratégia.
        """
        symbol = parameters.get("symbol", "N/A")
        high = parameters.get("high", None)
        low = parameters.get("low", None)
        current_price = parameters.get("current_price", None)
        
        if high is None or low is None or current_price is None:
            return {"error": "Parâmetros de preço incompletos para o breakout."}
        
        if current_price > high:
            signal = "buy"
        elif current_price < low:
            signal = "sell"
        else:
            signal = "hold"
        
        return {
            "status": "success",
            "symbol": symbol,
            "signal": signal,
            "details": f"Breakout analisado: Preço atual {current_price}, máxima {high}, mínima {low}."
        }
