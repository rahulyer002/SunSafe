<template>
    <div class="card">
        <h3>📍 Location</h3>
        <p><strong>📳 Status:</strong> {{ locationStatus }}</p>
        <!-- <p v-if="latitude && longitude">
            <strong>🗺️ Coordinates:</strong> {{ latitude }}, {{ longitude }}
        </p> -->
        <p v-if="timezone">
            <strong>🏙 Timezone:</strong> {{ timezone }}
        </p>
        <p v-if="temperature !== null">
            <strong>🌡️ Temperature:</strong> {{ temperature }}°C
        </p>
        <!-- <p v-if="humidity !== null">
            <strong>💧 Humidity:</strong> {{ humidity }}%
        </p>
        <p v-if="windSpeed !== null">
            <strong>🌬️ Wind Speed:</strong> {{ windSpeed }} m/s
        </p> -->
        <p v-if="weatherDesc">
            <strong>🌤️ Weather:</strong> {{ weatherDesc }}
        </p>
        <img v-if="icon" :src="getWeatherIconUrl(icon)" class="weather-bg-icon" />
    </div>
</template>

<script setup>
defineProps({
    locationStatus: String,
    latitude: Number,
    longitude: Number,
    temperature: Number,
    humidity: Number,
    windSpeed: Number,
    weatherDesc: String,
    icon: String,
    timezone: String
})

function getWeatherIconUrl(iconCode) {
    return `https://openweathermap.org/img/wn/${iconCode}@2x.png`
}

</script>

<style scoped>
/* .card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
} */

.card {
    position: relative;
    overflow: hidden;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    background: linear-gradient(135deg, #87b4f9, #c3cfe2);
}

.weather-bg-icon {
    position: absolute;
    right: 20px;
    bottom: 20px;
    width: 200px;
    opacity: 1.0;
    z-index: 0;
    pointer-events: none;
}
</style>