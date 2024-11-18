// backend/controllers/robotController.js

import OperationHistoryModel from '../models/OperationHistoryModel';

// Função para validar se o ID é válido
const isValidRobotId = (robotId) => {
    return /^[a-fA-F0-9]{24}$/.test(robotId); // Exemplo de validação para ID do MongoDB
};

// Função para buscar o histórico de operações de um robô
const getOperationHistory = async (req, res) => {
    const { robotId } = req.params;

    if (!isValidRobotId(robotId)) {
        return res.status(400).json({ error: "ID do robô inválido." });
    }

    try {
        const history = await OperationHistoryModel.find({ robotId });

        if (history.length === 0) {
            return res.status(404).json({ error: "Histórico de operações não encontrado para o robô fornecido." });
        }

        res.json({ history });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Erro ao buscar histórico de operações." });
    }
};

export { getOperationHistory };
