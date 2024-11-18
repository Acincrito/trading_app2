// frontend/src/services/api.js
import axiosInstance from './axios';  // Importando a instância do Axios

// Função genérica para fazer requisições com axios
const makeRequest = async (method, url, data = null) => {
    try {
        const response = await axiosInstance({
            method,   // Tipo de requisição (GET, POST, PUT, DELETE)
            url,       // URL do endpoint
            data,      // Dados para POST ou PUT
        });
        return response.data;  // Retorna os dados da resposta
    } catch (error) {
        // Melhorando o tratamento de erro para incluir mais detalhes
        console.error(`Erro ao fazer ${method} para ${url}:`, error.response ? error.response.data : error.message);
        throw new Error(`Erro ao fazer ${method} para ${url}`);
    }
};

// Função para buscar a lista de robôs
export const fetchRobots = async () => {
    return await makeRequest('GET', '/listagem');
};

// Função para buscar o histórico de operações de um robô
export const fetchOperations = async (robotId) => {
    return await makeRequest('GET', `/operations/${robotId}`);
};

// Função para atualizar o nome e a estratégia de um robô
export const updateRobot = async (robotId, data) => {
    return await makeRequest('PUT', `/robots/${robotId}`, data);
};

// Função para remover um robô
export const deleteRobot = async (robotId) => {
    return await makeRequest('DELETE', `/robots/${robotId}`);
};
