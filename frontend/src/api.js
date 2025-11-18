import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  register: (data) => api.post('/api/auth/register', data),
  getMe: () => api.get('/api/auth/me'),
};

// Portfolio API
export const portfolioAPI = {
  list: () => api.get('/api/portfolios/'),
  get: (id) => api.get(`/api/portfolios/${id}`),
  create: (data) => api.post('/api/portfolios/', data),
  update: (id, data) => api.put(`/api/portfolios/${id}`, data),
  delete: (id) => api.delete(`/api/portfolios/${id}`),
};

// Asset API
export const assetAPI = {
  listByPortfolio: (portfolioId) => api.get(`/api/assets/portfolio/${portfolioId}`),
  get: (id) => api.get(`/api/assets/${id}`),
  create: (data) => api.post('/api/assets/', data),
  update: (id, data) => api.put(`/api/assets/${id}`, data),
  delete: (id) => api.delete(`/api/assets/${id}`),
};

// Transaction API
export const transactionAPI = {
  listByPortfolio: (portfolioId) => api.get(`/api/transactions/portfolio/${portfolioId}`),
  listByAsset: (assetId) => api.get(`/api/transactions/asset/${assetId}`),
  create: (data) => api.post('/api/transactions/', data),
  delete: (id) => api.delete(`/api/transactions/${id}`),
};

// Price API
export const priceAPI = {
  update: (assetId, price, source = 'Manual') =>
    api.post(`/api/prices/update/${assetId}`, { asset_id: assetId, price, source }),
  updatePortfolio: (portfolioId) =>
    api.post(`/api/prices/update-portfolio/${portfolioId}`),
  getHistory: (assetId, days = 30) =>
    api.get(`/api/prices/history/${assetId}?days=${days}`),
};

// Import API
export const importAPI = {
  tradeRepublic: (portfolioId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/api/import/trade-republic/${portfolioId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  generic: (portfolioId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/api/import/generic-csv/${portfolioId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getTemplate: (type) => api.get(`/api/import/template/${type}`),
};

// Backup API
export const backupAPI = {
  exportAll: () => api.get('/api/backup/export/all', { responseType: 'blob' }),
  exportPortfolio: (portfolioId) =>
    api.get(`/api/backup/export/portfolio/${portfolioId}`, { responseType: 'blob' }),
  import: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/backup/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default api;
