# /backend/main.py
from data_handler.binance_client import BinanceClient
from data_handler.iq_option_client import IQOptionClient
from data_handler.mt5_client import MetaTrader5Client
from config.config import API_KEY, SECRET_KEY, BINANCE_URL, IQ_OPTION_URL, MT5_URL

def main():
    try:
        # Inicializando os clientes para cada plataforma
        binance_client = BinanceClient(BINANCE_URL, API_KEY, SECRET_KEY)
        iq_option_client = IQOptionClient(IQ_OPTION_URL, API_KEY)
        mt5_client = MetaTrader5Client(MT5_URL, API_KEY)

        # Solicitação das informações do usuário
        platform = input("Escolha a plataforma (binance, iq_option, mt5): ").strip().lower()
        symbol = input("Digite o símbolo do ativo (ex: BTC/USD): ").strip().upper()
        action = input("Digite a ação (compra/venda): ").strip().lower()
        try:
            amount = float(input("Digite o valor: "))
            if amount <= 0:
                raise ValueError("O valor deve ser positivo.")
        except ValueError as e:
            print(f"Erro: {e}")
            return

        # Executando a operação com base na plataforma escolhida
        response = None
        if platform == "binance":
            response = binance_client.execute_trade(symbol, action, amount)
        elif platform == "iq_option":
            response = iq_option_client.execute_trade(symbol, action, amount)
        elif platform == "mt5":
            response = mt5_client.execute_trade(symbol, action, amount)
        else:
            print("Plataforma não suportada. Escolha entre 'binance', 'iq_option' ou 'mt5'.")
            return

        # Exibindo a resposta da operação
        print("Resposta da operação:", response)

    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
