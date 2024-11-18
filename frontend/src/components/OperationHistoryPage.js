// frontend/src/components/OperationHistoryPage.js

import React, { useEffect, useState } from "react";
import { fetchOperations } from "../services/api";  // Função que busca o histórico de operações

const OperationHistoryPage = ({ robotId }) => {
    const [operations, setOperations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Função assíncrona para buscar os dados
        const fetchData = async () => {
            try {
                const response = await fetchOperations(robotId);
                setOperations(response);  // Assume que a resposta seja diretamente o array de operações
            } catch (error) {
                setError("Erro ao buscar histórico de operações");
                console.error("Erro ao buscar histórico de operações:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [robotId]);

    // Exibição condicional do conteúdo
    return (
        <div className="operation-history-page">
            <h2>Histórico de Operações</h2>

            {/* Exibição de carregamento, erro ou histórico */}
            {loading ? (
                <p>Carregando...</p>
            ) : error ? (
                <p>{error}</p>
            ) : operations.length === 0 ? (
                <p>Não há operações registradas para este robô.</p>
            ) : (
                <div className="operations-list">
                    {operations.map((operation) => (
                        <div key={operation.id} className="operation-item">
                            <p><strong>Lucro/Perda:</strong> {operation.profit_loss}</p>
                            <p><strong>Data:</strong> {new Date(operation.timestamp).toLocaleString()}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default OperationHistoryPage;
