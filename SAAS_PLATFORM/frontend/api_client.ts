import axios from 'axios';

// -----------------------------------------------------------------------------
// 🌍 CONFIGURAÇÃO DE AMBIENTE (Crucial)
// -----------------------------------------------------------------------------
// O Vite expõe variáveis do arquivo .env via import.meta.env.
// Crie um arquivo .env na raiz do frontend com: VITE_API_URL=http://localhost:8000
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log(`🔌 Conectando API em: ${API_URL}`);

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// -----------------------------------------------------------------------------
// 🛡️ INTERCEPTORS (Opcional, mas útil para Auth)
// -----------------------------------------------------------------------------
// Adiciona token JWT automaticamente se existir no localStorage
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Trata erros globais (ex: 401 Logout)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            console.warn('🔒 Sessão expirada ou inválida.');
            // window.location.href = '/login'; // Opcional: Redirecionar
        }
        return Promise.reject(error);
    }
);
