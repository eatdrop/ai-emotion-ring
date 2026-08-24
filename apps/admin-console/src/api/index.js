/**
 * RingHealth Admin API 瀹㈡埛绔?
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'

const BASE_URL = '/api'  // 閫氳繃vite proxy杞彂

const http = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' }
})

// 璇锋眰鎷︽埅鍣?
http.interceptors.request.use(config => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => Promise.reject(error))

// 鍝嶅簲鎷︽埅鍣?
http.interceptors.response.use(
  res => {
    if (res.data?.success === false) {
      ElMessage.error(res.data?.error || '璇锋眰澶辫触')
      return Promise.reject(new Error(res.data?.error))
    }
    return res.data
  },
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }
    ElMessage.error(err.message || '缃戠粶閿欒')
    return Promise.reject(err)
  }
)

// ==================== 缁熻鎺ュ彛 ====================
export function getStats() { return http.get('/v1/stats') }

// ==================== 鐢ㄦ埛绠＄悊 ====================
export function getAdminUsers(params) {
  return http.get('/v1/admin/users', { params })
}

// ==================== 鎯呯华鎶ヨ〃 ====================
export function getAdminEmotionStats() {
  return http.get('/v1/admin/emotions')
}

// ==================== 璁惧绠＄悊 ====================
export default http

