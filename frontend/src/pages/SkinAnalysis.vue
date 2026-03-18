<template>
      <div>
        <NavBar />
    </div>
  <div class="analysis-page">
    <div class="page-shell">
      <div class="header">
        <div class="title-wrap">
          <span class="badge">US 2.2</span>
          <h1>Skin Health Analysis</h1>
        </div>
        <p class="subtitle">Real-time database integration for personalised UV risk insights</p>
      </div>

      <div class="glass-card skin-card">
        <div class="card-head">
          <h2>Select Your Skin Tone</h2>
          <p>Choose the tone closest to yours to personalise the database mapping.</p>
        </div>

        <div class="skin-icons-container">
          <div
            v-for="type in skinTypes"
            :key="type.id"
            :class="['skin-icon', { active: form.skinType === type.id }]"
            :style="{ backgroundColor: type.color }"
            @click="selectSkin(type.id)"
          >
            <span class="type-label">Type {{ type.id }}</span>
          </div>
        </div>

        <div class="info-strip">
          <span class="info-label">Selected:</span>
          <span class="info-value">{{ selectedSkinDesc }}</span>
          <span class="divider"></span>
          <span class="info-label">Database Mapping:</span>
          <span class="info-value tone-pill">{{ toneCategory }}</span>
        </div>
      </div>

      <div class="glass-card uv-card" :style="{ borderTopColor: uvSeverityColor }">
        <div class="card-head">
          <h2>UV Exposure Level</h2>
          <p>Adjust the UV index to see how the projected risk changes.</p>
        </div>

        <div class="control-item">
          <div class="uv-label-row">
            <label>Adjust UV Index</label>
            <span class="uv-number" :style="{ color: uvSeverityColor }">{{ form.uvIndex }}</span>
          </div>

          <input
            type="range"
            min="1"
            max="11"
            v-model.number="form.uvIndex"
            @input="updateChart"
            class="uv-slider"
          />
        </div>

        <div class="db-result-box" :style="{ borderColor: uvSeverityColor, backgroundColor: uvSeverityColor + '12' }">
          <div class="result-item">
            <span class="label">Database Risk Level</span>
            <span class="value" :style="{ color: uvSeverityColor }">{{ apiRiskLevel }}</span>
          </div>
        </div>
      </div>

      <div class="glass-card chart-card">
        <div class="card-head">
          <h2>Risk Trend Over Time</h2>
          <p>Estimated exposure-related risk growth across a 60-minute period.</p>
        </div>
        <div ref="chartDom" class="chart-dom"></div>
      </div>

      <div class="glass-card insight-card">
        <div class="insight-header">
          <span class="icon">💡</span>
          <div>
            <h3>Safety Recommendation</h3>
            <p class="insight-subtitle">Based on your selected skin type and UV conditions</p>
          </div>
        </div>
        <p class="analysis-text">{{ analysisMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavBar from '../components/NavBar.vue'
import { ref, onMounted, reactive, computed, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';

const chartDom = ref(null);
let myChart = null;
const backendData = ref([]);

const form = reactive({
  skinType: 1,
  uvIndex: 8
});

const skinTypes = [
  { id: 1, color: '#F9EAD3', name: 'Very Fair' },
  { id: 2, color: '#F3D9B5', name: 'Fair' },
  { id: 3, color: '#E1B894', name: 'Medium' },
  { id: 4, color: '#B58150', name: 'Olive' },
  { id: 5, color: '#724628', name: 'Brown' },
  { id: 6, color: '#312529', name: 'Black' }
];

const handleResize = () => {
  if (myChart) {
    myChart.resize();
  }
};

onMounted(async () => {
  myChart = echarts.init(chartDom.value);
  updateChart();
  window.addEventListener('resize', handleResize);

  try {
    const response = await axios.get('https://sunsafe-zku7.onrender.com/skin/');
    backendData.value = response.data;
  } catch (error) {
    console.error('API Connection Error:', error);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (myChart) {
    myChart.dispose();
  }
});

const toneCategory = computed(() => {
  if (form.skinType <= 2) return 'Fair';
  if (form.skinType <= 4) return 'Medium';
  return 'Dark';
});

const apiRiskLevel = computed(() => {
  if (backendData.value.length === 0) return 'Connecting...';

  const match = backendData.value.find((item) => {
    return (
      item.skin_tone === toneCategory.value &&
      form.uvIndex >= item.uv_index_min &&
      form.uvIndex <= item.uv_index_max
    );
  });

  return match ? match.predicted_damage : 'Calculating...';
});

const uvSeverityColor = computed(() => {
  if (form.uvIndex <= 2) return '#22c55e';
  if (form.uvIndex <= 5) return '#eab308';
  if (form.uvIndex <= 7) return '#f97316';
  if (form.uvIndex <= 10) return '#ef4444';
  return '#a855f7';
});

const selectedSkinDesc = computed(() => {
  const type = skinTypes.find((t) => t.id === form.skinType);
  return type ? type.name : '';
});

const analysisMessage = computed(() => {
  const burnTime = Math.max(8, Number((150 / (form.uvIndex * (7 - form.skinType))).toFixed(0)));
  return `Database confirms a "${apiRiskLevel.value}" risk level for your ${toneCategory.value} skin tone. At UV ${form.uvIndex}, cumulative damage may begin in about ${burnTime} minutes. Consider sunscreen, shade, and protective clothing if you are staying outdoors.`;
});

const selectSkin = (id) => {
  form.skinType = id;
  updateChart();
};

const updateChart = () => {
  if (!myChart) return;

  const sensitivity = 7 - form.skinType;
  const dataPoints = [0.1, 0.25, 0.45, 0.7, 0.85, 1.0].map((val) =>
    Number((val * form.uvIndex * sensitivity).toFixed(2))
  );

  myChart.setOption({
    grid: {
      top: 30,
      left: 40,
      right: 20,
      bottom: 35
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.96)',
      borderColor: uvSeverityColor.value,
      borderWidth: 1,
      textStyle: { color: '#0f172a' },
      formatter: (params) => `Exposure: ${params[0].name}<br/>Risk Index: ${params[0].value}`
    },
    xAxis: {
      type: 'category',
      data: ['10m', '20m', '30m', '40m', '50m', '60m'],
      axisLabel: { color: '#64748b' },
      axisLine: { lineStyle: { color: '#cbd5e1' } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#64748b' },
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#e2e8f0' } }
    },
    series: [
      {
        data: dataPoints,
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          color: uvSeverityColor.value,
          width: 4
        },
        itemStyle: {
          color: uvSeverityColor.value
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: `${uvSeverityColor.value}55` },
            { offset: 1, color: 'rgba(255,255,255,0)' }
          ])
        }
      }
    ]
  });
};
</script>

<style scoped>
.analysis-page {
  min-height: 100vh;
  padding: 40px 20px;
  background:
    radial-gradient(circle at top left, rgba(59, 130, 246, 0.08), transparent 28%),
    radial-gradient(circle at top right, rgba(168, 85, 247, 0.08), transparent 24%),
    linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
  color: #0f172a;
}

.page-shell {
  max-width: 980px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 28px;
}

.title-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 999px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  color: #ffffff;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.18);
}

.header h1 {
  margin: 0;
  font-size: 2.1rem;
  font-weight: 800;
  color: #0f172a;
}

.subtitle {
  margin-top: 12px;
  font-size: 0.95rem;
  color: #64748b;
}

.glass-card {
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 20px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow:
    0 10px 30px rgba(15, 23, 42, 0.08),
    0 2px 8px rgba(15, 23, 42, 0.04);
}

.card-head {
  margin-bottom: 18px;
}

.card-head h2 {
  margin: 0 0 6px;
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
}

.card-head p {
  margin: 0;
  font-size: 0.92rem;
  color: #64748b;
}

.skin-icons-container {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  margin: 24px 0 34px;
  flex-wrap: wrap;
}

.skin-icon {
  width: 52px;
  height: 52px;
  border-radius: 999px;
  border: 3px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  flex-shrink: 0;
}

.skin-icon:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 10px 18px rgba(15, 23, 42, 0.12);
}

.skin-icon.active {
  border-color: #f59e0b;
  transform: scale(1.16);
  box-shadow: 0 0 0 6px rgba(245, 158, 11, 0.14);
}

.type-label {
  position: absolute;
  bottom: -26px;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
}

.info-strip {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 14px 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(248, 250, 252, 0.95), rgba(241, 245, 249, 0.95));
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.info-label {
  font-size: 0.9rem;
  color: #64748b;
}

.info-value {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
}

.tone-pill {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.08);
  color: #2563eb;
}

.divider {
  width: 1px;
  height: 18px;
  background: #cbd5e1;
}

.uv-card {
  border-top: 6px solid #cbd5e1;
}

.control-item {
  margin-top: 8px;
}

.uv-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.uv-label-row label {
  font-size: 0.96rem;
  font-weight: 600;
  color: #334155;
}

.uv-number {
  font-size: 1.25rem;
  font-weight: 800;
}

.uv-slider {
  width: 100%;
  accent-color: #f59e0b;
  cursor: pointer;
}

.db-result-box {
  margin-top: 22px;
  padding: 16px 18px;
  border-radius: 18px;
  border: 1px solid transparent;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.result-item .label {
  color: #475569;
  font-weight: 600;
}

.result-item .value {
  font-size: 1.2rem;
  font-weight: 900;
}

.chart-card {
  overflow: hidden;
}

.chart-dom {
  width: 100%;
  height: 340px;
}

.insight-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.86), rgba(248, 250, 252, 0.94));
}

.insight-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}

.icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(245, 158, 11, 0.12);
  font-size: 1.2rem;
}

.insight-header h3 {
  margin: 0;
  color: #f59e0b;
  font-size: 1.08rem;
}

.insight-subtitle {
  margin: 4px 0 0;
  font-size: 0.85rem;
  color: #64748b;
}

.analysis-text {
  margin: 0;
  line-height: 1.8;
  color: #334155;
  font-size: 0.98rem;
}

@media (max-width: 768px) {
  .analysis-page {
    padding: 24px 14px;
  }

  .header h1 {
    font-size: 1.7rem;
  }

  .glass-card {
    padding: 18px;
    border-radius: 20px;
  }

  .skin-icons-container {
    justify-content: center;
  }

  .result-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .uv-label-row {
    gap: 12px;
  }
}
</style>