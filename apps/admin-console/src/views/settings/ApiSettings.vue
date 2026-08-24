<template>
  <div class="api-settings-page">
    <el-card shadow="never">
      <template #header><span>API 鎺ュ彛绠＄悊</span></template>
      
      <!-- API绔偣鍒楄〃 -->
      <h4 style="margin:0 0 16px;color:#374151;">鎺ュ彛鍒楄〃</h4>
      
      <el-table :data="apiEndpoints" stripe size="small" border>
        <el-table-column prop="method" label="Method" width="90">
          <template #default="{ row }">
            <el-tag
              :type="row.method === 'GET' ? 'success' : row.method === 'POST' ? 'primary' : 'warning'"
              size="small"
            >{{ row.method }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="path" label="璺緞" min-width="240">
          <template #default="{ row }"><code>{{ row.path }}</code></template>
        </el-table-column>
        <el-table-column prop="desc" label="璇存槑" min-width="200" />
        <el-table-column prop="auth" label="璁よ瘉" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.auth ? 'danger' : 'info'" size="small">{{ row.auth ? '闇€' : '鍏? }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="鐘舵€? width="80" align="center">
          <template><el-tag type="success" size="small">姝ｅ父</el-tag></template>
        </el-table-column>
      </el-table>

      <el-divider />

      <!-- API娴嬭瘯宸ュ叿 -->
      <h4 style="margin:0 0 14px;color:#374151;">鎺ュ彛璋冭瘯</h4>
      
      <el-form :model="testForm" label-width="100px" size="default">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="閫夋嫨鎺ュ彛">
              <el-select v-model="testForm.path" placeholder="閫夋嫨瑕佹祴璇曠殑鎺ュ彛" style="width:100%;">
                <el-option
                  v-for="ep in testableEndpoints"
                  :key="ep.path"
                  :label="`${ep.method} ${ep.path}`"
                  :value="ep.path"
                />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="6">
            <el-form-item label="璇锋眰鍙傛暟">
              <el-input v-model="testForm.params" type="textarea" :rows="2"
                placeholder='{"heart_rate": 85, "user_id": "4698"}' />
            </el-form-item>
          </el-col>

          <el-col :span="4">
            <el-form-item label=" ">
              <el-button type="primary" @click="testApi" :loading="testing">
                鍙戦€佽姹?
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <!-- 娴嬭瘯缁撴灉 -->
      <div v-if="apiTestResult" class="test-result">
        <div class="result-header">
          <span>鍝嶅簲缁撴灉</span>
          <span :class="'status-' + (apiTestResult.ok ? 'ok' : 'err')">
            {{ apiTestResult.status }} {{ apiTestResult.statusText }}
          </span>
        </div>
        <pre class="result-body">{{ formatJson(apiTestResult.body) }}</pre>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const testing = ref(false)
const apiTestResult = ref(null)

const testForm = reactive({
  path: '/api/v1/health',
  params: ''
})

const apiEndpoints = [
  { method: 'GET', path: '/health', desc: '鍋ュ悍妫€鏌?, auth: false },
  { method: 'POST', path: '/api/v1/auth/login', desc: '鐢ㄦ埛鐧诲綍', auth: false },
  { method: 'POST', path: '/api/v1/auth/register', desc: '鐢ㄦ埛娉ㄥ唽', auth: false },
  { method: 'POST', path: '/api/v1/biometric', desc: '涓婁紶蹇冪巼鏁版嵁', auth: true },
  { method: 'POST', path: '/api/v1/predict', desc: '鎯呯华棰勬祴', auth: true },
  { method: 'GET', path: '/api/v1/latest/<uid>', desc: '鏈€鏂版暟鎹煡璇?, auth: true },
  { method: 'GET', path: '/api/v1/history/<uid>', desc: '鍘嗗彶璁板綍', auth: true },
  { method: 'GET', path: '/api/v1/stats', desc: '缁熻姒傝', auth: false },
  { method: 'GET', path: '/api/v1/baseline/<uid>', desc: '鐢ㄦ埛鍩虹嚎', auth: true },
  { method: 'POST', path: '/api/v1/device/bind', desc: '缁戝畾璁惧', auth: true },
  { method: 'GET', path: '/api/v1/admin/users', desc: '鐢ㄦ埛鍒楄〃(鍚庡彴)', auth: false },
  { method: 'GET', path: '/api/v1/admin/emotions', desc: '鎯呯华缁熻(鍚庡彴)', auth: false }
]

const testableEndpoints = apiEndpoints.filter(e => !['<uid>'].some(p => e.path.includes(p)))

async function testApi() {
  if (!testForm.path) return
  
  testing.value = true
  apiTestResult.value = null
  
  try {
    const method = apiEndpoints.find(e => e.path === testForm.path)?.method || 'GET'
    
    let body
    let headers = {}
    
    if (method === 'POST' && testForm.params) {
      body = JSON.parse(testForm.params)
      headers['Content-Type'] = 'application/json'
    }
    
    const options = { method, headers }
    if (body) options.body = JSON.stringify(body)
    
    const res = await fetch(testForm.path, options)
    
    const resBody = await res.json().catch(() => res.text())
    
    apiTestResult.value = {
      ok: res.ok,
      status: res.status,
      statusText: res.statusText,
      body: resBody
    }
  } catch(e) {
    apiTestResult.value = {
      ok: false,
      status: 0,
      statusText: e.message,
      body: e.toString()
    }
  } finally {
    testing.value = false
  }
}

function formatJson(data) {
  try {
    return typeof data === 'string' ? data : JSON.stringify(data, null, 2)
  } catch(e) {
    return String(data)
  }
}
</script>

<style scoped>
.test-result {
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}
.result-header {
  display: flex;
  justify-content: space-between;
  padding: 12px 18px;
  background: #f9fafb;
  font-weight: 600;
  font-size: 14px;
}
.status-ok { color: #059669; }
.status-err { color: #dc2626; }
.result-body {
  padding: 18px;
  font-family: 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 400px;
  overflow-y: auto;
  background: #fff;
  color: #374151;
}
</style>

