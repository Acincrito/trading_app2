import React, { useState } from 'react';
import axios from 'axios';

function RobotCard({ robot }) {
    const [status, setStatus] = useState(robot.status);

    const toggleStatus = async () => {
        const response = await axios.put(`/api/robots/${robot.id}/toggle`);
        setStatus(response.data.status);
    };

    const getHistory = async () => {
        const response = await axios.get(`/api/robots/${robot.id}/history`);
        alert(JSON.stringify(response.data));  // Mostra o histórico em um alert, pode ser melhorado
    };

    return (
        <div className="robot-card">
            <h3>{robot.name}</h3>
            <p>Status: {status}</p>
            <button onClick={toggleStatus}>{status === 'on' ? 'Desligar' : 'Ligar'}</button>
            <button onClick={getHistory}>Ver Histórico</button>
        </div>
    );
}

export default RobotCard;
