// frontend/src/components/RobotListPage.js

import React, { useState, useEffect } from "react";
import { fetchRobots, deleteRobot } from "../services/api";  // Funções que buscam e excluem robôs

const RobotListPage = () => {
    const [robots, setRobots] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetchRobots();
            setRobots(response);  // Assume que a resposta seja diretamente o array de robôs
        };
        fetchData();
    }, []);

    // Função para remover robô
    const removeRobot = async (robotId) => {
        try {
            await deleteRobot(robotId);  // Chama o endpoint DELETE
            setRobots(robots.filter((r) => r.id !== robotId));  // Remove o robô da lista local
        } catch (error) {
            console.error("Erro ao remover o robô:", error);
        }
    };

    return (
        <div>
            <h2>Lista de Robôs</h2>
            {robots.length === 0 ? (
                <p>Não há robôs cadastrados.</p>
            ) : (
                robots.map((robot) => (
                    <div key={robot.id}>
                        <span>{robot.name}</span>
                        <button onClick={() => removeRobot(robot.id)}>Excluir</button>
                    </div>
                ))
            )}
        </div>
    );
};

export default RobotListPage;
