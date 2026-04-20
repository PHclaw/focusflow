import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((cfg) => {
  const token = useAuthStore.getState().token
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

export const authApi = {
  register: (data: { email: string; username: string; password: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}

export const focusApi = {
  start: (data: { focus_type: string; duration_minutes: number }) =>
    api.post('/focus/start', data),
  complete: (sessionId: number, completed: boolean = true) =>
    api.post(`/focus/complete?session_id=${sessionId}&completed=${completed}`),
  dailyStats: () => api.get('/focus/stats/daily'),
  weeklyStats: () => api.get('/focus/stats/weekly'),
}

export const soundsApi = {
  list: () => api.get('/sounds/'),
  unlocked: () => api.get('/sounds/unlocked'),
  unlock: (soundId: number) => api.post(`/sounds/unlock/${soundId}`),
}

export const achievementsApi = {
  list: () => api.get('/achievements/'),
  earned: () => api.get('/achievements/earned'),
}

export default api
