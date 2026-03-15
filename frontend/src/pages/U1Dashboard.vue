<template>
    <div class="container">
        <h1>SunSafe Dashboard 🕶</h1>
        <p class="subtitle">
            Real-time UV monitoring and protection advice
        </p>

        <WeatherCard :location-status="locationStatus" :latitude="latitude" :longitude="longitude"
            :temperature="temperature" :humidity="humidity" :wind-speed="windSpeed" :weather-desc="weatherDesc"
            :icon="icon" :timezone="timezone" />

        <UVCard :loading="loading" :error="error" :uv-index="uvIndex" :risk-level="riskLevel" :advice="advice"
            :risk-color-class="riskColorClass" />

        <ProtectionList :uv-index="uvIndex" :risk-level="riskLevel" />
    </div>
    <p class="update-time">
        Last updated: {{ lastUpdated }}
    </p>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import WeatherCard from '../components/WeatherCard.vue'
import UVCard from '../components/UVCard.vue'
import ProtectionList from '../components/ProtectionList.vue'
import { fetchCurrentUV } from '../services/uvService'
import { getRiskLevel, getProtectionAdvice, getRiskColorClass } from '../utils/uvHelpers'

const latitude = ref(null)
const longitude = ref(null)
const temperature = ref(null)
const humidity = ref(null)
const windSpeed = ref(null)
const weatherDesc = ref('')
const icon = ref('')
const timezone = ref('')
const uvIndex = ref(null)
const loading = ref(false)
const error = ref('')
const locationStatus = ref('Waiting for location permission...')
const lastUpdated = ref('')

const riskLevel = computed(() =>
    uvIndex.value !== null ? getRiskLevel(uvIndex.value) : ''
)

const riskColorClass = computed(() =>
    getRiskColorClass(riskLevel.value)
)

const advice = computed(() =>
    uvIndex.value !== null ? getProtectionAdvice(uvIndex.value) : ''
)

function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by this browser'))
            return
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                })
            },
            (err) => reject(err)
        )
    })
}

async function loadUVData() {
    try {
        loading.value = true
        error.value = ''
        locationStatus.value = 'Getting your location...'

        const coords = await getUserLocation()
        latitude.value = coords.lat
        longitude.value = coords.lon
        locationStatus.value = 'Location received'

        const data = await fetchCurrentUV(coords.lat, coords.lon)
        temperature.value = Math.round(data.current?.temp ?? 0) ?? null
        humidity.value = data.current?.humidity ?? null
        icon.value = data.current?.weather?.[0]?.icon ?? ''
        windSpeed.value = data.current?.wind_speed ?? null
        timezone.value = data.timezone ?? ''

        weatherDesc.value =
            data.current?.weather?.[0]?.description ?? ''
        uvIndex.value = data.current?.uvi ?? null
        lastUpdated.value = new Date().toLocaleTimeString()

        if (uvIndex.value === null) {
            throw new Error('UV index not found in API response')
        }
    } catch (err) {
        error.value = err.message || 'Something went wrong'
        locationStatus.value = 'Failed to get location or UV data'
    } finally {
        loading.value = false
    }
}

let refreshTimer = null

onMounted(() => {
    loadUVData()

    refreshTimer = setInterval(() => {
        loadUVData()
    }, 600000)  
})
</script>

<style>
.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}

.subtitle {
    color: #666;
    margin-top: -10px;
    margin-bottom: 25px;
}

.update-time {
    margin-top: 15px;
    font-size: 13px;
    color: #888;
}
</style>