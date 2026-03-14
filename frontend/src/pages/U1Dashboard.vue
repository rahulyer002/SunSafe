<template>
    <div class="container">
        <h1>SunSafe Dashboard</h1>

        <WeatherCard :location-status="locationStatus" :latitude="latitude" :longitude="longitude"
            :temperature="temperature" :humidity="humidity" :wind-speed="windSpeed" :weather-desc="weatherDesc" />

        <UVCard :loading="loading" :error="error" :uv-index="uvIndex" :risk-level="riskLevel" :advice="advice" :risk-color-class="riskColorClass" />

        <ProtectionList :uv-index="uvIndex" :risk-level="riskLevel" />
    </div>
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
const uvIndex = ref(null)
const loading = ref(false)
const error = ref('')
const locationStatus = ref('Waiting for location permission...')

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

        windSpeed.value = data.current?.wind_speed ?? null

        weatherDesc.value =
            data.current?.weather?.[0]?.description ?? ''
        uvIndex.value = data.current?.uvi ?? null

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

onMounted(() => {
    loadUVData()
})
</script>

<style>
.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}
</style>