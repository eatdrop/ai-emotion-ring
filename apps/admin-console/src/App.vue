<template>
  <el-container class="app-container">
    <!-- 渚ц竟鏍?-->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
      <div class="logo-area">
        <span class="logo-icon">馃拲</span>
        <transition name="fade">
          <span v-show="!isCollapse" class="logo-text">鏄熸灑鍋ュ悍</span>
        </transition>
      </div>

      <el-menu
        :default-active="currentRoute"
        :collapse="isCollapse"
        router
        background-color="#1e293b"
        text-color="#94a3b8"
        active-text-color="#fff"
        active-background-color="transparent"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>鏁版嵁鐪嬫澘</template>
        </el-menu-item>

        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <template #title>鐢ㄦ埛绠＄悊</template>
        </el-menu-item>

        <el-menu-item index="/devices">
          <el-icon><Monitor /></el-icon>
          <template #title>璁惧绠＄悊</template>
        </el-menu-item>

        <el-menu-item index="/emotion-report">
          <el-icon><TrendCharts /></el-icon>
          <template #title>鎯呯华鎶ヨ〃</template>
        </el-menu-item>

        <el-sub-menu index="system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>绯荤粺璁剧疆</span>
          </template>
          <el-menu-item index="/settings/model">妯″瀷閰嶇疆</el-menu-item>
          <el-menu-item index="/settings/api">API绠＄悊</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <!-- 涓诲尯鍩?-->
    <el-container>
      <!-- 椤舵爮 -->
      <el-header class="header">
        <div class="header-left">
          <el-icon 
            class="collapse-btn" 
            @click="isCollapse = !isCollapse"
          >
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">棣栭〉</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="header-right">
          <el-badge :value="0" :max="99" class="notice-badge">
            <el-icon :size="20"><Bell /></el-icon>
          </el-badge>
          
          <el-dropdown @command="handleCommand">
            <span class="user-dropdown">
              <el-avatar :size="32" style="background: linear-gradient(135deg, #6366f1, #a78bfa);">
                绠?
              </el-avatar>
              <span class="user-name">绠＄悊鍛?/span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">涓汉涓績</el-dropdown-item>
                <el-dropdown-item divided command="logout">閫€鍑虹櫥褰?/el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 鍐呭鍖?-->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)

const currentRoute = computed(() => route.path)
const currentRouteName = computed(() => {
  const map = {
    '/dashboard': '鏁版嵁鐪嬫澘',
    '/users': '鐢ㄦ埛绠＄悊',
    '/devices': '璁惧绠＄悊',
    '/emotion-report': '鎯呯华鎶ヨ〃',
    '/settings/model': '妯″瀷閰嶇疆',
    '/settings/api': 'API绠＄悊'
  }
  return map[route.path] || route.meta?.title || ''
})

function handleCommand(cmd) {
  if (cmd === 'logout') {
    localStorage.removeItem('admin_token')
    router.push('/login')
  }
}
</script>

<style scoped>
.app-container { height: 100vh; }

/* 渚ц竟鏍?*/
.sidebar {
  background: #1e293b;
  overflow: hidden;
  transition: width 0.28s;
  box-shadow: 4rpx 0 16rpx rgba(0,0,0,0.1);
}
.logo-area {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 22rpx 18rpx;
  height: 60px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.logo-icon { font-size: 26px; flex-shrink: 0; }
.logo-text {
  font-size: 19px;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
  letter-spacing: 2px;
}

/* 椤堕儴瀵艰埅鏍?*/
.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid #f1f5f9;
  box-shadow: 0 1rpx 4rpx rgba(0,0,0,0.04);
  height: 56px;
}
.header-left { display: flex; align-items: center; gap: 16px; }
.collapse-btn { font-size: 22px; cursor: pointer; color: #64748b; transition: color 0.2s; }
.collapse-btn:hover { color: #6366f1; }

.header-right { display: flex; align-items: center; gap: 24px; }
.notice-badge { cursor: pointer; color: #64748b; }
.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #374151;
}
.user-name { font-size: 14px; font-weight: 500; }

/* 涓诲唴瀹瑰尯 */
.main-content {
  background: #f8fafc;
  padding: 24px;
  min-height: calc(100vh - 56px);
  overflow-y: auto;
}

/* 鍔ㄧ敾 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.fade-transform-enter-active,
.fade-transform-leave-active { transition: all 0.25s ease; }
.fade-transform-enter-from { opacity: 0; transform: translateX(-12px); }
.fade-transform-leave-to { opacity: 0; transform: translateX(12px); }

/* 鑿滃崟鏍峰紡瑕嗙洊 */
:deep(.el-menu) { border-right: none !important; }
:deep(.el-menu-item) { margin: 4px 8px; border-radius: 10px; }
:deep(.el-menu-item.is-active) { 
  background: linear-gradient(135deg, #6366f1, #818cf8) !important;
  border-radius: 10px !important;
}
</style>

