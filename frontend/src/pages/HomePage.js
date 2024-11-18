// frontend/src/pages/HomePage.js

import React from 'react';
import TradingControls from '../components/TradingControls';
import OperationHistory from '../components/OperationHistory';

// HomePage componente
const HomePage = () => {
    return (
        <div className="home-page">
            <header>
                <h1>Bem-vindo ao Gerenciador de Robôs de Trading</h1>
                <p className="subtitle">
                    Controle e visualize o desempenho dos seus robôs de trading de forma fácil e eficiente.
                </p>
            </header>

            <section className="controls-section">
                <h2>Controles de Trading</h2>
                <TradingControls />
            </section>

            <section className="history-section">
                <h2>Histórico de Operações</h2>
                <OperationHistory />
            </section>
        </div>
    );
};

export default HomePage;
