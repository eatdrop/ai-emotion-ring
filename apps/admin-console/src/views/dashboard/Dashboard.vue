<template>
  <div class="dashboard">
    <!-- 缁熻鍗＄墖琛?-->
    <el-row :gutter="20" class="stat-cards">
      <el-col :xs="12" :sm="6" v-for="(stat, idx) in statCards" :key="idx">
        <div class="stat-card" :style="{ borderTopColor: stat.color }">
          <div class="card-icon-wrap" :style="{ background: stat.color + '10' }">
            <span style="font-size: 28px;">{{ stat.icon }}</span>
          </div>
          <div class="card-info">
            <span class="card-value">{{ stat.value }}</span>
            <span class="card-label">{{ stat.label }}</span>
          </div>
          <div class="card-trend" :class="stat.trend > 0 ? 'trend-up' : 'trend-down'">
            <el-icon><TopRight v-if="stat.trend > 0" /><BottomRight v-else /></el-icon>
            <span>{{ Math.abs(stat.trend) }}%</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 鍥捐〃鍖哄煙 -->
    <el-row :gutter="20" style="margin-top: 24px;">
      <!-- 鎯呯华鍒嗗竷楗煎浘 -->
      <el-col :xs="24" :lg="8">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header"><span>鎯呯华鍒嗗竷</span></div>
          </template>
          <div ref="pieChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>

      <!-- 姣忔棩瓒嬪娍鎶樼嚎鍥?-->
      <el-col :xs="24" :lg="16">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>鏁版嵁瓒嬪娍 (杩?0澶?</span>
              <el-radio-group v-model="chartRange" size="small">
                <el-radio-button value="7">7澶?/el-radio-button>
                <el-radio-button value="14">14澶?/el-radio-button>
                <el-radio-button value="30">30澶?/el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="lineChartRef" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搴曢儴鍖哄煙 -->
    <el-row :gutter="20" style="margin-top: 24px;">
      <!-- 鏈€杩戠敤鎴峰垪琛?-->
      <el-col :xs="24" :lg="12">
        <el-card shadow="never">
          <template #header>
            <div class="card-header"><span>鏈€杩戞敞鍐岀敤鎴?/span></div>
          </template>
          <el-table :data="recentUsers" size="small" stripe>
            <el-table-column prop="nickname" label="鏄电О" />
            <el-table-column prop="phone" label="鎵嬫満鍙? width="130">
              <template #default="{ row }">
                {{ maskPhone(row.phone) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="娉ㄥ唽鏃堕棿" width="170">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="鐘舵€? width="80">
              <template #default>
                <el-tag type="success" size="small">姝ｅ父</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 绯荤粺淇℃伅 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="never">
          <template #header>
            <div class="card-header"><span>绯荤粺鐘舵€?/span></div>
          </template>
          <div class="system-info">
            <div class="info-item" v-for="(item, idx) in systemItems" :key="idx">
              <span class="info-label">{{ item.label }}</span>
              <span class="info-value" :style="{ color: item.color }">
                <el-icon v-if="item.icon === 'check'" style="color: #10b981;"><CircleCheck /></el-icon>
                {{ item.value }}
              </span>
            </div>
          </div>

          <el-divider />

          <div class="quick-actions">
            <el-button type="primary" @click="refreshData" :loading="loading">
              <el-icon><Refresh /></el-icon> 鍒锋柊鏁版嵁
            </el-button>
            <el-button @click="exportReport">
              <el-icon><Download /></el-icon> 瀵煎嚭鎶ヨ〃
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getStats, getAdminUsers } from '../../api/index.js'

const loading = ref(false)
const chartRange = ref('7')
const pieChartRef = ref(null)
const lineChartRef = ref(null)
let pieChart = null
let lineChart = null

// 缁熻鍗＄墖
const statCards = ref([
  { icon: '馃懃', label: '鎬荤敤鎴锋暟', value: '--', color: '#6366f1', trend: 12 },
  { icon: '馃拲', label: '鍦ㄧ嚎璁惧', value: '--', color: '#10b981', trend: 5 },
  { icon: '馃搳', label: '浠婃棩鏁版嵁', value: '--', color: '#f59e0b', trend: -3 },
  { icon: '馃', label: '鍒嗘瀽鎬绘暟', value: '--', color: '#ef4444', trend: 18 }
])

// 鏈€杩戠敤鎴?
const recentUsers = ref([])

// 绯荤粺鐘舵€?
const systemItems = ref([
  { label: 'API鏈嶅姟', value: '杩愯涓?, color: '#10b981', icon: 'check' },
  { label: '鎯呯华妯″瀷', value: '宸插姞杞?, color: '#6366f1' },
  { label: '瀛樺偍妯″紡', value: 'JSON', color: '#94a3b8' },
  { label: '鐗堟湰鍙?, value: 'v1.0.0', color: '#94a3b8' }
])

async function loadDashboard() {
  loading.value = true
  
  try {
    // 鍔犺浇缁熻鏁版嵁
    const statsRes = await getStats()
    
    if (statsRes?.data) {
      const d = statsRes.data
      
      statCards.value[0].value = d.total_users || 0
      statCards.value[1].value = d.online_devices || 0
      statCards.value[2].value = d.last_24h_records || 0
      statCards.value[3].value = d.total_analyzed || 0
      
      // 鏇存柊绯荤粺鐘舵€?
      systemItems.value[1].value = d.model_loaded ? '宸插姞杞? : '鏈姞杞?
      systemItems.value[1].color = d.model_loaded ? '#10b981' : '#f59e0b'
      systemItems.value[2].value = (d.storage_backend || 'JSON').toUpperCase()
      
      // 缁樺埗鍥捐〃
      await nextTick()
      renderPieChart(d.emotion_distribution || {})
    }

    // 鍔犺浇鏈€杩戠敤鎴?
    try {
      const usersRes = await getAdminUsers({ limit: 5 })
      recentUsers.value = usersRes?.data || []
    } catch(e) {
      console.warn('鍔犺浇鐢ㄦ埛澶辫触:', e)
    }
    
  } catch(e) {
    console.error('浠〃鐩樺姞杞藉け璐?', e)
  } finally {
    loading.value = false
  }
}

function renderPieChart(dist) {
  if (!pieChartRef.value) return
  
  pieChart = echarts.init(pieChartRef.value)
  
  pieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: '5%', itemWidth: 16, itemHeight: 16 },
    color: ['#10b981', '#f59e0b', '#ef4444'],
    series: [{
      type: 'pie',
      radius: ['45%', '72%'],
      center: ['50%', '48%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      emphasis: {
        label: {
          show: true,
          fontSize: 18,
          fontWeight: 'bold',
          formatter: '{d}%'
        }
      },
      data: [
        { name: '骞抽潤', value: dist.calm || 0 },
        { name: '鐒﹁檻', value: dist.anxious || 0 },
        { name: '鍏村', value: dist.excited || 0 }
      ]
    }]
  })
}

function renderLineChart() {
  if (!lineChartRef.value) return
  
  lineChart = echarts.init(lineChartRef.value)
  
  // 妯℃嫙瓒嬪娍鏁版嵁锛堝疄闄呭簲浠嶢PI鑾峰彇锛?
  const days = parseInt(chartRange.value)
  const dates = []
  const calmData = []
  const anxiousData = []
  
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    dates.push(`${d.getMonth()+1}/${d.getDate()}`)
    calmData.push(Math.floor(Math.random() * 40 + 15))
    anxiousData.push(Math.floor(Math.random() * 15 + 3))
  }
  
  lineChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['骞抽潤', '鐒﹁檻'], bottom: '5%' },
    grid: { top: '12%', left: '3%', right: '4%', bottom: '18%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: dates, axisLabel: { fontSize: 11 } },
    yAxis: { type: 'value', axisLabel: { formatter: '{value}' } },
    color: ['#10b981', '#f59e0b'],
    series: [
      { name: '骞抽潤', type: 'line', smooth: true, areaStyle: { opacity: 0.12 }, data: calmData },
      { name: '鐒﹁檻', type: 'line', smooth: true, areaStyle: { opacity: 0.08 }, data: anxiousData }
    ]
  })
}

function refreshData() {
  loadDashboard().then(() => renderLineChart())
}

function exportReport() {
  // TODO: 瀹炵幇瀵煎嚭鍔熻兘
  window.open('/api/v1/admin/emotions/export')
}

function maskPhone(phone) {
  if (!phone || phone.length < 11) return phone
  return phone.substring(0, 3) + '****' + phone.substring(7)
}

function formatDate(dateStr) {
  if (!dateStr) return '--'
  try {
    return new Date(dateStr).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
  } catch(e) { return dateStr }
}

onMounted(async () => {
  await loadDashboard()
  await nextTick()
  renderLineChart()
})

onUnmounted(() => {
  pieChart?.dispose()
  lineChart?.dispose()
})
</script>

<style scoped>
.stat-cards { margin-bottom: 0; }
.stat-card {
  background: #fff;
  border-radius: 14px;
  padding: 22rpx;
  display: flex;
  align-items: center;
  gap: 16px;
  border-top: 4px solid #6366f1;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.card-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.card-info { flex: 1; }
.card-value { font-size: 28px; font-weight: 800; color: #1e293b; display: block; line-height: 1.2; }
.card-label { font-size: 13px; color: #94a3b8; display: block; margin-top: 2px; }
.card-trend {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 8px;
}
.trend-up { background: #ecfdf5; color: #059669; }
.trend-down { background: #fef2f2; color: #dc2626; }

.chart-card { border-radius: 14px; overflow: hidden; }
.card-header { display: flex; justify-content: space-between; align-items: center; font-weight: 600; }

.system-info { display: flex; flex-direction: column; gap: 14px; }
.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f8fafc;
}
.info-item:last-child { border-bottom: none; }
.info-label { font-size: 14px; color: #64748b; }
.info-value { font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; }

.quick-actions { display: flex; gap: 12px; }
</style>

