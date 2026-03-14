<template>
  <div class="analysis-page">
    <div class="header">
      <h1>Skin Health Analysis</h1>
      <p class="subtitle">Personalized for your unique skin profile (US 2.2)</p>
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
          :title="type.name"
        >
          <span class="type-label">Type {{ type.id }}</span>
        </div>
      </div>
      <p class="skin-desc">{{ selectedSkinDesc }}</p>
    </div>

    <div class="glass-card uv-display-card" :style="{ borderLeftColor: uvSeverityColor }">
      <div class="control-item">
        <label>Adjust UV Index: <span :style="{ color: uvSeverityColor, fontWeight: 'bold' }">{{ form.uvIndex }}</span></label>
        <input 
          type="range" 
          min="1" 
          max="11" 
          v-model.number="form.uvIndex" 
          @input="updateChart"
          class="uv-slider"
        >
      </div>
      <div class="uv-status" :style="{ backgroundColor: uvSeverityColor + '22', color: uvSeverityColor }">
        Risk Level: {{ uvRiskLevel }}
      </div>
    </div>

    <div class="glass-card chart-container">
      <div ref="chartDom" style="width: 100%; height: 300px;"></div>
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

const chartDom = ref(null);
let myChart = null;

// Static data for skin types based on Fitzpatrick Scale
const skinTypes = [
  { id: 1, color: '#F9EAD3', name: 'Very Fair' },
  { id: 2, color: '#F3D9B5', name: 'Fair' },
  { id: 3, color: '#E1B894', name: 'Medium' },
  { id: 4, color: '#B58150', name: 'Olive' },
  { id: 5, color: '#724628', name: 'Brown' },
  { id: 6, color: '#312529', name: 'Black' }
];

const form = reactive({
  skinType: 1,
  uvIndex: 8
});

// Logic for UV Risk Level and Colors (Standard Australian UV scale)
const uvRiskLevel = computed(() => {
  if (form.uvIndex <= 2) return 'Low';
  if (form.uvIndex <= 5) return 'Moderate';
  if (form.uvIndex <= 7) return 'High';
  if (form.uvIndex <= 10) return 'Very High';
  return 'Extreme';
});

const uvSeverityColor = computed(() => {
  if (form.uvIndex <= 2) return '#4ade80'; // Green
  if (form.uvIndex <= 5) return '#fde047'; // Yellow
  if (form.uvIndex <= 7) return '#fb923c'; // Orange
  if (form.uvIndex <= 10) return '#ef4444'; // Red
  return '#a855f7'; // Purple (Extreme)
});

const selectedSkinDesc = computed(() => {
  const type = skinTypes.find(t => t.id === form.skinType);
  return type ? `${type.name} skin tone selected.` : '';
});

const selectSkin = (id) => {
  form.skinType = id;
  updateChart();
};

// ... keep previous analysisMessage logic ...
const analysisMessage = computed(() => {
  const riskFactor = form.skinType * (12 - form.uvIndex);
  const burnTime = Math.max(8, (150 / (form.uvIndex * (7 - form.skinType))).toFixed(0));

  if (riskFactor < 15 || form.skinType <= 2) {
    return `Critical Warning: Your skin has very low melanin protection. Damage can begin in just ${burnTime} minutes at this UV level. [cite: 30, 46]`;
  }
  return `Note: While your skin has some protection, UV Index ${form.uvIndex} still poses cumulative risks. Reapply sunscreen regularly. [cite: 52]`;
});

// ... keep previous updateChart logic ...
/**
 * Function: updateChart
 * Updates the ECharts instance and configures the tooltip for data display.
 * Aligned with US 2.1: Visualizing UV impacts.
 */
const updateChart = () => {
  if (!myChart) return;

  const timeLabels = ['10m', '20m', '30m', '40m', '50m', '60m'];
  const sensitivity = (7 - form.skinType); 
  const dataPoints = [0.1, 0.25, 0.45, 0.7, 0.85, 1.0].map(val => 
    (val * form.uvIndex * sensitivity).toFixed(2)
  );

  const option = {
    title: { 
      text: 'Predicted Damage Accumulation', 
      textStyle: { color: '#fff', fontSize: 16 } 
    },
    
    tooltip: { 
      trigger: 'axis',
      backgroundColor: 'rgba(30, 41, 59, 0.9)', // 
      borderColor: uvSeverityColor.value,
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const data = params[0];
        return `
          <div style="padding: 5px;">
            <b style="color:${uvSeverityColor.value}">Exposure: ${data.name}</b><br/>
            Risk Index: ${data.value}<br/>
            <small>Status: ${uvRiskLevel.value}</small>
          </div>
        `;
      }
    },
    grid: { left: '10%', right: '10%', bottom: '15%' },
    xAxis: { 
      type: 'category', 
      data: timeLabels, 
      axisLabel: { color: '#fff' } 
    },
    yAxis: { 
      type: 'value', 
      name: 'Risk Index', 
      axisLabel: { color: '#fff' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
    },
    series: [{
      name: 'UV Damage',
      data: dataPoints,
      type: 'line',
      smooth: true,
      lineStyle: { color: uvSeverityColor.value, width: 4 },
      symbol: 'circle', // 
      symbolSize: 8,
      itemStyle: { color: uvSeverityColor.value },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: `${uvSeverityColor.value}66` },
          { offset: 1, color: 'transparent' }
        ])
      }
    }]
  };

  myChart.setOption(option);
};

onMounted(() => {
  myChart = echarts.init(chartDom.value);
  updateChart();
});
</script>

<style scoped>
.analysis-page { padding: 20px; background: #0f172a; min-height: 100vh; color: white; }
.glass-card { background: rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; margin-bottom: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }

/* Skin Icons Layout */
.skin-icons-container { display: flex; justify-content: space-between; margin: 15px 0; }
.skin-icon {
  width: 45px; height: 45px; border-radius: 50%; border: 3px solid transparent; 
  cursor: pointer; transition: all 0.3s; position: relative;
}
.skin-icon.active { border-color: #fbbf24; transform: scale(1.15); box-shadow: 0 0 15px #fbbf2455; }
.type-label { position: absolute; bottom: -20px; left: 0; width: 100%; font-size: 10px; text-align: center; }
.skin-desc { font-size: 0.8rem; opacity: 0.7; text-align: center; margin-top: 25px; }

/* UV Card specific styling */
.uv-display-card { border-left: 6px solid #ccc; transition: border-color 0.5s ease; }
.uv-status { padding: 8px 15px; border-radius: 10px; font-weight: bold; margin-top: 10px; text-align: center; }
.uv-slider { width: 100%; height: 8px; border-radius: 5px; appearance: none; background: #334155; }
.uv-slider::-webkit-slider-thumb { appearance: none; width: 20px; height: 20px; background: white; border-radius: 50%; cursor: pointer; }
</style>