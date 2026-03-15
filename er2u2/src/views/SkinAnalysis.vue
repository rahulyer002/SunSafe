<template>
  <div class="analysis-page">
    <div class="header">
      <h1>Skin Health Analysis</h1>
      <p class="subtitle">Real-time database integration (US 2.2)</p>
    </div>

    <div class="glass-card">
      <label class="section-label">Select Your Skin Tone</label>
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
      <p class="skin-desc">{{ selectedSkinDesc }} (Mapped to <b>{{ toneCategory }}</b> for Database)</p>
    </div>

    <div class="glass-card uv-display-card" :style="{ borderLeftColor: uvSeverityColor }">
      <div class="control-item">
        <label>Adjust UV Index: <span :style="{ color: uvSeverityColor, fontWeight: 'bold' }">{{ form.uvIndex }}</span></label>
        <input 
          type="range" min="1" max="11" 
          v-model.number="form.uvIndex" 
          @input="updateChart"
          class="uv-slider"
        >
      </div>
      
      <div class="db-result-box" :style="{ backgroundColor: uvSeverityColor + '15' }">
        <div class="result-item">
          <span class="label">Database Risk Level:</span>
          <span class="value" :style="{ color: uvSeverityColor }">{{ apiRiskLevel }}</span>
        </div>
      </div>
    </div>

    <div class="glass-card chart-container">
      <div ref="chartDom" style="width: 100%; height: 320px;"></div>
    </div>

    <div class="glass-card insight">
      <div class="insight-header">
        <span class="icon">💡</span>
        <h3>Safety Recommendation</h3>
      </div>
      <p class="analysis-text">{{ analysisMessage }}</p>
    </div>
  </div>
</template>

<script setup>
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

onMounted(async () => {
  // Initialize ECharts instance
  myChart = echarts.init(chartDom.value);
  updateChart();
  window.addEventListener('resize', () => myChart && myChart.resize());

  try {
    // Fetching data from your Render backend
    const response = await axios.get('https://sunsafe-zku7.onrender.com/skin/');
    backendData.value = response.data;
  } catch (error) {
    console.error("API Connection Error:", error);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', () => myChart && myChart.resize());
  if (myChart) myChart.dispose();
});

/**
 * Maps Fitzpatrick scale (1-6) to backend categories (Fair/Medium/Dark)
 * Based on the structure in your JSON screenshot.
 */
const toneCategory = computed(() => {
  if (form.skinType <= 2) return "Fair";
  if (form.skinType <= 4) return "Medium";
  return "Dark";
});

/**
 * Filters backendData to find the matching predicted_damage
 * Matches both the mapped skin_tone and the UV range.
 */
const apiRiskLevel = computed(() => {
  if (backendData.value.length === 0) return "Connecting...";

  const match = backendData.value.find(item => {
    return item.skin_tone === toneCategory.value && 
           form.uvIndex >= item.uv_index_min && 
           form.uvIndex <= item.uv_index_max;
  });

  return match ? match.predicted_damage : "Calculating...";
});

/**
 * Dynamic color calculation based on UV Index severity
 */
const uvSeverityColor = computed(() => {
  if (form.uvIndex <= 2) return '#4ade80';
  if (form.uvIndex <= 5) return '#fde047';
  if (form.uvIndex <= 7) return '#fb923c';
  if (form.uvIndex <= 10) return '#ef4444';
  return '#a855f7';
});

const selectedSkinDesc = computed(() => {
  const type = skinTypes.find(t => t.id === form.skinType);
  return type ? type.name : '';
});

/**
 * Relatable language generation combining burn time and backend risk levels
 */
const analysisMessage = computed(() => {
  const burnTime = Math.max(8, (150 / (form.uvIndex * (7 - form.skinType))).toFixed(0));
  return `Database confirms a "${apiRiskLevel.value}" risk level for your ${toneCategory.value} skin tone. At UV ${form.uvIndex}, cumulative damage begins in ${burnTime} minutes.`;
});

const selectSkin = (id) => {
  form.skinType = id;
  updateChart();
};

/**
 * Updates the chart data points and theme color
 */
const updateChart = () => {
  if (!myChart) return;
  const sensitivity = (7 - form.skinType); 
  const dataPoints = [0.1, 0.25, 0.45, 0.7, 0.85, 1.0].map(val => (val * form.uvIndex * sensitivity).toFixed(2));

  myChart.setOption({
    tooltip: { 
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: uvSeverityColor.value,
      textStyle: { color: '#fff' },
      formatter: (params) => `Exposure: ${params[0].name}<br/>Risk Index: ${params[0].value}`
    },
    xAxis: { 
      type: 'category', 
      data: ['10m', '20m', '30m', '40m', '50m', '60m'], 
      axisLabel: { color: '#94a3b8' } 
    },
    yAxis: { 
      type: 'value', 
      axisLabel: { color: '#94a3b8' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
    },
    series: [{
      data: dataPoints,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { color: uvSeverityColor.value, width: 4 },
      itemStyle: { color: uvSeverityColor.value },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: `${uvSeverityColor.value}66` },
          { offset: 1, color: 'transparent' }
        ])
      }
    }]
  });
};
</script>

<style scoped>
.analysis-page { padding: 20px; background: #0f172a; min-height: 100vh; color: white; }
.header { text-align: center; margin-bottom: 30px; }
.subtitle { opacity: 0.5; font-size: 0.85rem; }

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(15px);
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 20px;
  border: 1px solid rgba(255,255,255,0.08);
}

.skin-icons-container { display: flex; justify-content: space-between; margin: 25px 0; }
.skin-icon {
  width: 44px; height: 44px; border-radius: 50%; border: 3px solid transparent; 
  cursor: pointer; transition: 0.4s; position: relative;
}
.skin-icon.active { border-color: #fbbf24; transform: scale(1.25); box-shadow: 0 0 20px rgba(251,191,36,0.3); }
.type-label { position: absolute; bottom: -24px; left: 0; width: 100%; font-size: 10px; text-align: center; color: #64748b; }
.skin-desc { font-size: 0.8rem; text-align: center; margin-top: 30px; color: #64748b; }

.uv-display-card { border-left: 8px solid #ccc; transition: 0.6s ease; }
.db-result-box { margin-top: 20px; padding: 15px; border-radius: 16px; }
.result-item { display: flex; justify-content: space-between; align-items: center; }
.result-item .value { font-size: 1.2rem; font-weight: 900; }

.uv-slider { width: 100%; accent-color: #fbbf24; }

.insight-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.insight-header h3 { color: #fbbf24; margin: 0; font-size: 1.1rem; }
.analysis-text { line-height: 1.7; color: #cbd5e1; }
</style>