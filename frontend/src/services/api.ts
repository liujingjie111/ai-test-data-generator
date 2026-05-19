import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 如果是 401 错误且有无效的 API key，自动清除 localStorage
    if (error.response?.status === 401) {
      const message = error.response?.data?.message || ''
      if (message.includes('Invalid API key') || message.includes('API key')) {
        localStorage.removeItem('token')
        console.log('已清除无效的 API key')
      }
    }
    const message = error.response?.data?.message || error.message || '网络错误'
    return Promise.reject(new Error(message))
  },
)

export const generateWithAI = async (prompt: string, count: number, apiKey?: string, model?: string) => {
  const response = await api.post('/ai/generate', { prompt, count, api_key: apiKey, model });
  return response;
};

export default api
