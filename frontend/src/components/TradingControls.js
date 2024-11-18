// frontend/src/components/TradingControls.js

import React, { useState } from 'react';

const TradingControls = () => {
    const [isTrading, setIsTrading] = useState(false);

    // Função para alternar o estado do trading
    const toggleTrading = async () => {
        try {
            // Faz a requisição POST para iniciar ou parar o trading, dependendo do estado atual
            const response = await fetch(isTrading ? "/stop_trading/" : "/start_trading/", {
                method: "POST",
            });

            // Se a resposta for ok, alterna o estado de trading
            if (response.ok) {
                setIsTrading(prevState => !prevState);
            } else {
                console.error("Erro ao alterar o estado de trading");
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
        }
    };

    return (
        <div className="trading-controls">
            <button onClick={toggleTrading} className="btn btn-secondary">
                {isTrading ? "Parar Trading" : "Iniciar Trading"}
            </button>
        </div>
    );
};

export default TradingControls;
