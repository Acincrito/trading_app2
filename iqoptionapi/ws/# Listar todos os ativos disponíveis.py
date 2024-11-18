# Listar todos os ativos disponíveis
print("Ativos disponíveis:", OP_code.ACTIVES.keys())

for ativo in ativos['digital'].keys():
    print("Tentando obter payout para o ativo:", ativo)
    try:
        payout = Iq.get_digital_payout(ativo)
        if payout is not None:
            melhores_ativos.append((ativo, payout))
    except KeyError as e:
        logging.error(f"Erro ao obter payout para o ativo {ativo}: {e}")
        continue  # ou outra lógica de recuperação
