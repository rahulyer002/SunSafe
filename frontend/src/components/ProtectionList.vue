<template>
  <div class="card">
    <h3>Protective Actions</h3>

    <ul v-if="uvIndex !== null">
      <li v-for="item in actions" :key="item">
        {{ item }}
      </li>
    </ul>

    <p v-else>No UV data yet.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  uvIndex: Number,
  riskLevel: String
})

const actions = computed(() => {
  if (props.uvIndex === null || props.uvIndex === undefined) return []

  if (props.uvIndex <= 2) {
    return ['Safe outdoor exposure']
  }
  if (props.uvIndex <= 5) {
    return ['Apply sunscreen', 'Wear sunglasses']
  }
  if (props.uvIndex <= 7) {
    return ['Apply sunscreen', 'Seek shade', 'Wear protective clothing']
  }
  if (props.uvIndex <= 10) {
    return ['Limit sun exposure', 'Seek shade', 'Wear a hat']
  }
  return ['Immediate sun protection required', 'Avoid direct sunlight', 'Use sunscreen SPF 50+']
})
</script>

<style scoped>
.card {
  background: white;
  padding: 15px;
  border-radius: 15px;
  margin-bottom: 15px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
</style>