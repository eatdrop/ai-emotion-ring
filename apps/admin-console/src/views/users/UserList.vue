<template>
  <div class="user-list-page">
    <el-card shadow="never">
      <!-- 鎼滅储鏍?-->
      <div class="search-bar">
        <el-input
          v-model="keyword"
          placeholder="鎼滅储鏄电О/鎵嬫満鍙?
          clearable
          style="width: 280px;"
          @keyup.enter="searchUsers"
          @clear="searchUsers"
        >
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button type="primary" @click="searchUsers" :loading="loading">
          鎼滅储
        </el-button>
      </div>

      <!-- 鐢ㄦ埛琛ㄦ牸 -->
      <el-table :data="users" v-loading="loading" stripe size="default" row-key="_id">
        <el-table-column prop="nickname" label="鏄电О" min-width="120">
          <template #default="{ row }">
            <div class="user-cell">
              <el-avatar :size="36" :style="{ background: getAvatarColor(row.nickname) }">
                {{ (row.nickname || 'U')[0] }}
              </el-avatar>
              <span>{{ row.nickname || '--' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="phone" label="鎵嬫満鍙? width="150">
          <template #default="{ row }">{{ maskPhone(row.phone) }}</template>
        </el-table-column>

        <el-table-column label="鎬у埆/骞撮緞" width="110">
          <template #default="{ row }">
            {{ genderMap[row.gender] ?? '-' }} / {{ row.age ?? '-' }}
          </template>
        </el-table-column>

        <el-table-column label="浣撻噸(kg)" width="90">
          <template #default="{ row }">{{ row.weight_kg || '--' }}</template>
        </el-table-column>

        <el-table-column prop="created_at" label="娉ㄥ唽鏃堕棿" width="180">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>

        <el-table-column label="鎿嶄綔" width="160" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="showDetail(row)">璇︽儏</el-button>
            <el-button link type="warning" size="small" @click="editUser(row)">缂栬緫</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 鍒嗛〉 -->
      <div class="pagination-wrap" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 璇︽儏寮圭獥 -->
    <el-dialog v-model="detailVisible" title="鐢ㄦ埛璇︽儏" width="560px">
      <el-descriptions :column="2" border v-if="currentUser">
        <el-descriptions-item label="鐢ㄦ埛ID">{{ currentUser._id }}</el-descriptions-item>
        <el-descriptions-item label="鏄电О">{{ currentUser.nickname }}</el-descriptions-item>
        <el-descriptions-item label="鎵嬫満鍙?>{{ maskPhone(currentUser.phone, false) }}</el-descriptions-item>
        <el-descriptions-item label="鎬у埆">{{ genderMap[currentUser.gender] }}</el-descriptions-item>
        <el-descriptions-item label="骞撮緞">{{ currentUser.age || '鏈缃? }}宀?/el-descriptions-item>
        <el-descriptions-item label="浣撻噸">{{ currentUser.weight_kg ? currentUser.weight_kg + 'kg' : '鏈缃? }}</el-descriptions-item>
        <el-descriptions-item label="韬珮">{{ currentUser.height_cm ? currentUser.height_cm + 'cm' : '鏈缃? }}</el-descriptions-item>
        <el-descriptions-item label="娉ㄥ唽鏃堕棿">{{ formatDate(currentUser.created_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminUsers } from '../../api/index.js'

const loading = ref(false)
const keyword = ref('')
const users = ref([])
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)
const detailVisible = ref(false)
const currentUser = ref(null)

const genderMap = { 0: '濂?, 1: '鐢?, 2: '鍏朵粬' }

async function loadData(page = currentPage.value) {
  loading.value = true
  try {
    const res = await getAdminUsers({ page, limit: pageSize, keyword: keyword.value })
    
    if (res?.data) {
      users.value = res.data
      total.value = res.pagination?.total || 0
    }
  } catch(e) {
    console.error('鍔犺浇鐢ㄦ埛鍒楄〃澶辫触:', e)
  } finally {
    loading.value = false
  }
}

function searchUsers() { currentPage.value = 1; loadData() }

function showDetail(user) {
  currentUser.value = user
  detailVisible.value = true
}

function editUser(user) {
  // TODO: 瀹炵幇缂栬緫鍔熻兘
}

function maskPhone(phone, mask = true) {
  if (!phone || phone.length < 11) return phone || '--'
  return mask ? phone.substring(0,3)+'****'+phone.substring(7) : phone
}

function formatDate(dateStr) {
  if (!dateStr) return '--'
  try { return new Date(dateStr).toLocaleString('zh-CN') } catch(e) { return dateStr }
}

function getAvatarColor(name) {
  const colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
  const code = (name || '?').charCodeAt(0) || 0
  return colors[code % colors.length]
}

onMounted(() => loadData())
</script>

<style scoped>
.search-bar { display: flex; gap: 12px; margin-bottom: 20px; }

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}
.user-cell span { font-weight: 500; }

.pagination-wrap {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>

