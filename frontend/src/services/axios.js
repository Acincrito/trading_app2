// frontend/src/services/axios.js
import axios from 'axios';

// Criação da instância do axios com configurações básicas
const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api',  // URL do backend
    timeout: 5000,  // Timeout para requisições
    headers: {
        'Content-Type': 'application/json', // Cabeçalho de tipo de conteúdo padrão
        // 'Authorization': `Bearer ${localStorage.getItem('token')}` // Adicione o token se necessário
    },
});

// Interceptor para lidar com erros
axiosInstance.interceptors.response.use(
    response => response,  // Se a resposta for bem-sucedida, apenas retorna a resposta
    error => {
        // Manipulação de erro de requisição
        if (error.response) {
            // O servidor respondeu com um código de status fora da faixa de 2xx
            console.error('Erro na resposta:', error.response.data);
        } else if (error.request) {
            // A requisição foi feita, mas não houve resposta
            console.error('Erro na requisição:', error.request);
        } else {
            // Outro tipo de erro (configuração, etc.)
            console.error('Erro desconhecido:', error.message);
        }
        return Promise.reject(error);  // Rejeita a promise com o erro
    }
);

export default axiosInstance;
