// frontend/src/pages/OperationHistory.js
import React, { useEffect, useState } from "react";
import { fetchOperationHistory } from "../services/api";
import "./OperationHistory.css";


const OperationHistory = ({ robotId }) => {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        fetchOperationHistory(robotId).then(data => {
            if (data && data.history) {
                setHistory(data.history);
            }
        });
    }, [robotId]);

    return (
        <div>
            <h2>Histórico de Operações</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Profit/Loss</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {history.map(op => (
                        <tr key={op.id}>
                            <td>{op.id}</td>
                            <td>{op.profit_loss}</td>
                            <td>{op.timestamp}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OperationHistory;
