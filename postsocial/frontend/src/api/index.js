import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Создаем экземпляр axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Интерцептор для добавления токена
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Интерцептор для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  register(userData) {
    return apiClient.post('/auth/register', userData)
  },
  login(credentials) {
    return apiClient.post('/auth/login', new URLSearchParams(credentials), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  getMe() {
    return apiClient.get('/auth/me')
  },
  updateMe(userData) {
    return apiClient.put('/auth/me', userData)
  },
}

// Recipients API
export const recipientsApi = {
  getAll(params = {}) {
    return apiClient.get('/recipients/', { params })
  },
  getById(id) {
    return apiClient.get(`/recipients/${id}`)
  },
  create(data) {
    return apiClient.post('/recipients/', data)
  },
  update(id, data) {
    return apiClient.put(`/recipients/${id}`, data)
  },
  delete(id) {
    return apiClient.delete(`/recipients/${id}`)
  },
}

export default apiClient
