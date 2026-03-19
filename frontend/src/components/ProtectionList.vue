<template>
    <div class="card">
        <h3>⚠️ Protective Actions</h3>

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
        return ['Safe outdoor exposure','Wear sunglasses if sensitive to light']
    }
    if (props.uvIndex <= 5) {
        return ['Apply sunscreen SPF 30+', 'Wear sunglasses','Stay hydrated']
    }
    if (props.uvIndex <= 7) {
        return ['Apply sunscreen SPF 30+', 'Seek shade', 'Wear protective clothing','Avoid midday sun (11am–3pm)']
    }
    if (props.uvIndex <= 10) {
        return ['Limit sun exposure', 'Seek shade', 'Wear a wide-brim hat','Apply sunscreen SPF 50+']
    }
    return ['Immediate sun protection required', 'Avoid direct sunlight', 'Use sunscreen SPF 50+']
})
</script>

<style scoped>
.card {
    background: linear-gradient(135deg, #87b4f9, #87b4f9);
    padding: 15px;
    border-radius: 24px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    height: 100%;
}
</style>