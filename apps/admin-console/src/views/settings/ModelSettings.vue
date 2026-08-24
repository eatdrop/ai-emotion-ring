<template>
  <div class="model-settings-page">
    <el-card shadow="never">
      <template #header><span>鎯呯华璇嗗埆妯″瀷閰嶇疆</span></template>

      <el-descriptions :column="2" border title="妯″瀷鍩烘湰淇℃伅">
        <el-descriptions-item label="绠楁硶绫诲瀷">RandomForest</el-descriptions-item>
        <el-descriptions-item label="鍐崇瓥鏍戞暟閲?>200 妫?/el-descriptions-item>
        <el-descriptions-item label="鏈€澶ф繁搴?>12 灞?/el-descriptions-item>
        <el-descriptions-item label="鐗瑰緛缁村害">11 缁?/el-descriptions-item>
        <el-descriptions-item label="杈撳嚭绫诲埆">
          <el-tag size="small" type="success" style="margin-right:6px;">骞抽潤 calm</el-tag>
          <el-tag size="small" type="warning" style="margin-right:6px;">鐒﹁檻 anxious</el-tag>
          <el-tag size="small" type="danger">鍏村 excited</el-tag>
        </el-descriptions-item>
        <el-descriptions-item :label="'妯″瀷鐘舵€?">
          <el-tag :type="modelLoaded ? 'success' : 'danger'">{{ modelLoaded ? '宸插姞杞? : '鏈姞杞? }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <!-- 鐗瑰緛閲嶈鎬ц〃鏍?-->
      <h4 style="margin: 28px 0 16px; color: #374151;">鐗瑰緛閲嶈鎬ф帓鍚?/h4>
      <el-table :data="features" stripe size="small" max-height="400">
        <el-table-column prop="rank" label="#" width="50" align="center" />
        <el-table-column prop="name" label="鐗瑰緛鍚嶇О" min-width="180" />
        <el-table-column prop="importance" label="閲嶈鎬? width="160">
          <template #default="{ row }">
            <div style="display:flex;align-items:center;gap:8px;">
              <el-progress
                :percentage="(row.importance * 100).toFixed(1)"
                :stroke-width="10"
                :show-text="false"
                color="#6366f1"
                style="flex:1;"
              />
              <span style="width:55px;text-align:right;font-weight:600;color:#6366f1;font-size:13px;">
                {{ (row.importance * 100).toFixed(1) }}%
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="desc" label="璇存槑" />
      </el-table>

      <el-divider />

      <div class="actions">
        <el-button type="primary" @click="reloadModel">
          <el-icon><Refresh /></el-icon> 閲嶈浇妯″瀷
        </el-button>
        <el-button @click="testPredict">
          <el-icon><Cpu /></el-icon> 娴嬭瘯棰勬祴
        </el-button>
      </div>
    </el-card>

    <!-- 娴嬭瘯缁撴灉 -->
    <el-card shadow="never" style="margin-top:20px;" v-if="testResult">
      <template #header><span>棰勬祴娴嬭瘯缁撴灉</span></template>
      
      <el-result
        :icon="testResult.success ? 'success' : 'error'"
        :title="testResult.emotion || (testResult.error || '澶辫触')"
        :sub-title="testResult.subTitle || ''"
      >
        <template #extra v-if="testResult.data">
          <el-descriptions :column="1" size="small" border style="max-width:500px;margin:0 auto;">
            <el-descriptions-item label="鎯呯华鏍囩">{{ testResult.data.label }}</el-descriptions-item>
            <el-descriptions-item label="鎯呯华鍒嗘暟">{{ testResult.data.score }}</el-descriptions-item>
            <el-descriptions-item v-for="(v, k) in testResult.data.probs" :key="k" :label="k">{{ v }}</el-descriptions-item>
          </el-descriptions>
        </template>
      </el-result>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const modelLoaded = ref(false)
const testResult = ref(null)

const features = [
  { rank: 1, name: 'hrv_proxy', importance: 0.1904, desc: 'HRV浠ｇ悊鍊硷紙蹇冪巼鍙樺紓鎬э級' },
  { rank: 2, name: 'hr_baseline_deviation', importance: 0.1783, desc: '蹇冪巼鍋忕鍩虹嚎绋嬪害' },
  { rank: 3, name: 'hr_zscore', importance: 0.1706, desc: '蹇冪巼Z-score鏍囧噯鍖栧€? },
  { rank: 4, name: 'is_night', importance: 0.1660, desc: '鏄惁涓烘繁澶滄椂娈?0-5鐐?23鐐瑰悗)' },
  { rank: 5, name: 'heart_rate', importance: 0.1047, desc: '蹇冪巼缁濆鍊?BPM)' },
  { rank: 6, name: 'hr_ratio', importance: 0.0742, desc: '蹇冪巼/涓綅鏁版瘮鐜? },
  { rank: 7, name: 'hour_cos', importance: 0.0612, desc: '灏忔椂浣欏鸡缂栫爜' },
  { rank: 8, name: 'hour_sin', importance: 0.0472, desc: '灏忔椂姝ｅ鸡缂栫爜' },
  { rank: 9, name: 'weight_kg', importance: 0.0047, desc: '鐢ㄦ埛浣撻噸(kg)' },
  { rank: 10, name: 'age', importance: 0.0023, desc: '鐢ㄦ埛骞撮緞' },
  { rank: 11, name: 'gender', importance: 0.0005, desc: '鎬у埆(0=濂?1=鐢?2=鍏朵粬)' }
]

async function checkModel() {
  try {
    const res = await fetch('/health')
    if (res.ok) {
      const data = await res.json()
      modelLoaded.value = data.model_loaded ?? false
    }
  } catch(e) {}
}

async function reloadModel() {
  try {
    const res = await fetch('/api/v1/admin/reload-model', { method: 'POST' })
    if (res.ok) {
      ElMessage?.({ message: '妯″瀷閲嶈浇鎴愬姛', type: 'success' }) || alert('妯″瀷閲嶈浇鎴愬姛')
    }
  } catch(e) {
    ElMessage?.({ message: '閲嶈浇澶辫触', type: 'error' }) || alert('閲嶈浇澶辫触')
  }
}

async function testPredict() {
  try {
    const res = await fetch('/api/v1/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: '4698',
        heart_rate: Math.floor(Math.random() * 60 + 70),
        timestamp: new Date().toISOString(),
        gender: 1,
        age: 24,
        weight_kg: 72
      })
    })

    if (res.ok) {
      const data = await res.json()
      
      if (data.success !== false && data.data) {
        let extra = {}
        try { extra = JSON.parse(data.data.extra_result) } catch(e) {}
        
        testResult.value = {
          success: true,
          emotion: `鎯呯华: ${data.data.emotion_label}`,
          data: {
            label: data.data.emotion_label,
            score: `${((data.data.emotion_score||0)*100).toFixed(1)}%`,
            probs: extra.probabilities ? Object.entries(extra.probabilities).map(([k,v]) => `${k}: ${(v*100).toFixed(1)}%`).join(', ') : '--'
          }
        }
      } else {
        testResult.value = { success: false, error: data.error || '棰勬祴澶辫触' }
      }
    }
  } catch(e) {
    testResult.value = { success: false, error: e.message }
  }
}

onMounted(checkModel)
</script>

<style scoped>
.actions { display: flex; gap: 12px; }
</style>

