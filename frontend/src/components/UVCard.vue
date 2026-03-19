<template>
    <div class="uvCard" :class="riskColorClass">
        <h2>UV INDEX</h2>

        <p v-if="loading">Loading UV data...</p>
        <p v-else-if="error">Error: {{ error }}</p>

        <template v-else>
            <h1>{{ uvIndex }}</h1>
            <p>Risk Level: {{ riskLevel }}</p>
            <p v-if="humidity !== null">
                <strong>💧 Humidity:</strong> &nbsp&nbsp&nbsp{{ humidity }}%
            </p>
            <p v-if="windSpeed !== null">
                <strong>🌬️ Wind Speed:</strong> &nbsp&nbsp&nbsp{{ windSpeed }} m/s
            </p>
            <div class="adviceBox">
                <h3>☀️ Protection Advice:</h3>
                <p>{{ advice }}</p>
            </div>
        </template>
    </div>
</template>

<script setup>
defineProps({
    loading: Boolean,
    error: String,
    uvIndex: Number,
    riskLevel: String,
    advice: String,
    riskColorClass: String,
    humidity: Number,
    windSpeed: Number,
})
</script>

<style scoped>
.uvCard {
    padding: 20px;
    border-radius: 24px;
    color: white;
    text-align: center;
    transition: background 0.3s ease;
    height: 100%;
}


.adviceBox {
    margin-top: 15px;
    background: rgba(255, 255, 255, 0.15);
    padding: 12px;
    border-radius: 12px;
    text-align: left;
}


.uv-minimal {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.uv-low {
    background: linear-gradient(135deg, #cccc2e, #c5c532);
}

.uv-moderate {
    background: linear-gradient(135deg, #f1c40f, #f39c12);
    color: #222;
}

.uv-high {
    background: linear-gradient(135deg, #e67e22, #d35400);
}

.uv-very-high {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.uv-extreme {
    background: linear-gradient(135deg, #8e44ad, #6c3483);
}
</style>