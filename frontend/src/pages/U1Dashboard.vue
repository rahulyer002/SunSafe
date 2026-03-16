<template>
    <div class="container">
        <div class="background-video">
            <video autoplay muted loop playsinline>
                <source src="/background.mp4" type="video/mp4">
            </video>
        </div>
        <h1 style="font-size: 50px;">SunSafe Dashboard 🕶</h1>
        <p class="subtitle">
            Real-time UV monitoring and protection advice
        </p>
        <WeatherCard class="card-enter card-delay-1" :location-status="locationStatus" :latitude="latitude"
            :longitude="longitude" :temperature="temperature" :humidity="humidity" :wind-speed="windSpeed"
            :weather-desc="weatherDesc" :icon="icon" :timezone="timezone" />


        <UVCard class="card-enter card-delay-2" :loading="loading" :error="error" :uv-index="uvIndex"
            :risk-level="riskLevel" :advice="advice" :risk-color-class="riskColorClass" :humidity="humidity"
            :wind-speed="windSpeed" />

        <ProtectionList class="card-enter card-delay-3" :uv-index="uvIndex" :risk-level="riskLevel" />
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

.background-video {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
}

.background-video video {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card-enter {
    opacity: 0;
    transform: translateY(30px);
    animation: fadeUp 3s ease-out forwards;
}

.card-delay-1 {
    animation-delay: 0.1s;
}

.card-delay-2 {
    animation-delay: 0.4s;
}

.card-delay-3 {
    animation-delay: 0.7s;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>