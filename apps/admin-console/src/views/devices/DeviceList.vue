<template>
  <div class="device-list-page">
    <el-card shadow="never">
      <div class="page-header">
        <span class="header-title">璁惧绠＄悊</span>
        <el-button type="primary" size="small">
          <el-icon><Plus /></el-icon> 娣诲姞璁惧
        </el-button>
      </div>

      <!-- 璁惧琛ㄦ牸 -->
      <el-table :data="devices" v-loading="loading" stripe size="default">
        <el-table-column prop="device_id" label="璁惧ID" min-width="180">
          <template #default="{ row }">
            <code class="device-code">{{ row.device_id }}</code>
          </template>
        </el-table-column>

        <el-table-column prop="device_name" label="璁惧鍚嶇О" width="160" />

        <el-table-column prop="device_type" label="绫诲瀷" width="90">
          <template #default="{ row }">
            <el-tag :type="row.device_type === 'ring' ? 'primary' : 'info'" size="small">
              {{ row.device_type === 'ring' ? '鎴掓寚' : '鎵嬬幆' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="user_id" label="缁戝畾鐢ㄦ埛" width="120">
          <template #default="{ row }">{{ row.user_id || '--' }}</template>
        </el-table-column>

        <el-table-column label="鐘舵€? width="100">
          <template #default="{ row }">
            <el-tag
              :type="row.is_online && row.is_active ? 'success' : 'info'"
              size="small"
              effect="dark"
            >
              {{ (row.is_online && row.is_active) ? '鍦ㄧ嚎' : '绂荤嚎' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="bound_at" label="缁戝畾鏃堕棿" width="170">
          <template #default="{ row }">{{ formatDate(row.bound_at) }}</template>
        </el-table-column>

        <el-table-column prop="last_seen" label="鏈€鍚庢椿璺? width="170">
          <template #default="{ row }">{{ formatDate(row.last_seen) }}</template>
        </el-table-column>

        <el-table-column label="鎿嶄綔" width="140" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small">鏌ョ湅</el-button>
            <el-button
              link
              type="danger"
              size="small"
              @click="unbindDevice(row)"
              :disabled="!row.is_active"
            >
              瑙ｇ粦
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 绌虹姸鎬?-->
      <el-empty description="鏆傛棤璁惧鏁版嵁" v-if="!loading && devices.length === 0" />
    </el-card>

    <!-- BLE鍗忚淇℃伅鍗＄墖 -->
    <el-card shadow="never" style="margin-top: 20px;">
      <template #header><span>钃濈墮鍗忚鍙傛暟 (鎴掓寚)</span></template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="鏈嶅姟UUID"><code>0BC0</code></el-descriptions-item>
        <el-descriptions-item label="鍐欏叆鐗瑰緛UUID"><code>0BC1</code></el-descriptions-item>
        <el-descriptions-item label="閫氱煡鐗瑰緛UUID"><code>0BC2</code></el-descriptions-item>
        <el-descriptions-item label="蹇冪巼鏁版嵁鎸囦护"><code>0x0503</code></el-descriptions-item>
      </el-descriptions>

      <el-alert
        title="杩炴帴娴佺▼锛氭壂鎻?鏈嶅姟UUID=0BC0) 鈫?杩炴帴 鈫?璁㈤槄閫氱煡(0BC2) 鈫?鍙戦€佹寚浠?鍚?BC1鍐欏叆0x0503) 鈫?鎺ユ敹蹇冪巼鏁版嵁"
        type="info"
        :closable="false"
        style="margin-top: 16px;"
        show-icon
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(false)
const devices = ref([])

async function loadDevices() {
  loading.value = true
  try {
    // 浠嶢PI鍔犺浇鎴栦娇鐢ㄦā鎷熸暟鎹紙寮€鍙戦樁娈碉級
    const res = await fetch('/api/v1/admin/devices').catch(() => null)
    
    if (res?.ok) {
      const data = await res.json()
      devices.value = data.data || []
    } else {
      // 妯℃嫙鏁版嵁
      devices.value = [
        { device_id: 'RING-A1B2C3D4', device_name: '鏄熸灑鎸囩幆Pro', device_type: 'ring', user_id: 'U46980001', is_active: true, is_online: true, bound_at: '2026-05-28T10:00:00', last_seen: '2026-05-30T23:30:00' },
        { device_id: 'RING-E5F6G7H8', device_name: '鏄熸灑鎸囩幆Lite', device_type: 'ring', user_id: 'U46980002', is_active: true, is_online: false, bound_at: '2026-05-25T14:20:00', last_seen: '2026-05-29T18:45:00' }
      ]
    }
  } catch(e) {
    console.error('鍔犺浇璁惧澶辫触:', e)
    devices.value = []
  } finally {
    loading.value = false
  }
}

function unbindDevice(device) {
  // TODO: 瀹炵幇瑙ｇ粦閫昏緫
}

function formatDate(dateStr) {
  if (!dateStr) return '--'
  try { return new Date(dateStr).toLocaleString('zh-CN') } catch(e) { return dateStr }
}

onMounted(loadDevices)
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.header-title { font-size: 18px; font-weight: 700; color: #1e293b; }

.device-code {
  font-family: 'Monaco', monospace;
  font-size: 13px;
  background: #f1f5f9;
  padding: 3px 8px;
  border-radius: 6px;
}
</style>

