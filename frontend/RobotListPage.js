import { useEffect, useState } from "react";
import { fetchRobots, updateRobotStatus } from "../services/api";  // Funções de API

const RobotListPage = () => {
    const [robots, setRobots] = useState([]);
    const [loading, setLoading] = useState(true);  // Estado para o carregamento
    const [error, setError] = useState(null);  // Estado para erros

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetchRobots();
                setRobots(response.data);
            } catch (error) {
                setError("Erro ao carregar robôs");
            } finally {
                setLoading(false);  // Finaliza o carregamento
            }
        };
        fetchData();
    }, []);

    const toggleRobot = async (robotId) => {
        const robot = robots.find((r) => r.id === robotId);
        const newStatus = robot.status === "ON" ? "OFF" : "ON";

        try {
            await updateRobotStatus(robotId, newStatus);  // Atualiza o status no backend
            setRobots(robots.map(r => r.id === robotId ? { ...r, status: newStatus } : r));  // Atualiza o estado local
        } catch (error) {
            setError("Erro ao atualizar status do robô");
        }
    };

    if (loading) {
        return <div>Carregando robôs...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h2>Lista de Robôs</h2>
            {robots.length === 0 ? (
                <div>Sem robôs cadastrados.</div>
            ) : (
                robots.map((robot) => (
                    <div key={robot.id}>
                        <span>{robot.name}</span>
                        <button onClick={() => toggleRobot(robot.id)}>
                            {robot.status === "ON" ? "Desligar" : "Ligar"}
                        </button>
                    </div>
                ))
            )}
        </div>
    );
};

export default RobotListPage;
