import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/dashboard/Dashboard.vue'),
    meta: { title: '鏁版嵁鐪嬫澘' }
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/users/UserList.vue'),
    meta: { title: '鐢ㄦ埛绠＄悊' }
  },
  {
    path: '/devices',
    name: 'Devices',
    component: () => import('../views/devices/DeviceList.vue'),
    meta: { title: '璁惧绠＄悊' }
  },
  {
    path: '/emotion-report',
    name: 'EmotionReport',
    component: () => import('../views/emotion/EmotionReport.vue'),
    meta: { title: '鎯呯华鎶ヨ〃' }
  },
  {
    path: '/settings/model',
    name: 'ModelSettings',
    component: () => import('../views/settings/ModelSettings.vue'),
    meta: { title: '妯″瀷閰嶇疆' }
  },
  {
    path: '/settings/api',
    name: 'ApiSettings',
    component: () => import('../views/settings/ApiSettings.vue'),
    meta: { title: 'API绠＄悊' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

