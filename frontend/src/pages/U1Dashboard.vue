<template>
    <div>
        <NavBar />
    </div>>
    <div class="container">
        <h1 style="font-size: 50px;color: white;">SunSafe Dashboard 🕶</h1>
        <p class="subtitle">
            Your personal sun safety dashboard for real-time UV monitoring, weather insights, forecasts, and smart
            protection guidance.
        </p>

        <div class="search-bar">
            <input v-model="searchQuery" type="text" placeholder="Search city or suburb (e.g. Melbourne, Clayton)"
                @keyup.enter="handleSearch" />
            <button @click="handleSearch" :disabled="loading">
                Search
            </button>
            <button @click="loadCurrentLocationData" :disabled="loading">
                Use Current Location
            </button>
        </div>

        <p class="location-label">
            {{ locationStatus }}
        </p>

        <div class="main-layout">
            <div class="left-panel">
                <WeatherCard class="card-enter card-delay-1" :location-status="locationStatus" :latitude="latitude"
                    :longitude="longitude" :temperature="temperature" :humidity="humidity" :wind-speed="windSpeed"
                    :weather-desc="weatherDesc" :icon="icon" :timezone="timezone" />

                <div class="dashboard-row">
                    <UVCard class="card-enter card-delay-2 dashboard-card" :loading="loading" :error="error"
                        :uv-index="uvIndex" :risk-level="riskLevel" :advice="advice" :risk-color-class="riskColorClass"
                        :humidity="humidity" :wind-speed="windSpeed" />

                    <ProtectionList class="card-enter card-delay-3 dashboard-card" :uv-index="uvIndex"
                        :risk-level="riskLevel" />
                </div>
            </div>

            <div class="right-panel">
                <div class="future-card-placeholder card-enter card-delay-3">
                    <h3>Future Forecast</h3>

                    <div v-if="dailyForecast.length" class="forecast-list">
                        <div v-for="day in dailyForecast" :key="day.dt" class="forecast-item">
                            <div class="forecast-day">
                                <div class="weekday">
                                    {{ getWeekday(day.dt) }}
                                </div>

                                <div class="date">
                                    {{ getDate(day.dt) }}
                                </div>
                            </div>

                            <img :src="`https://openweathermap.org/img/wn/${day.weather?.[0]?.icon}@2x.png`"
                                :alt="day.weather?.[0]?.description || 'weather icon'" class="forecast-icon" />

                            <div class="forecast-temp">
                                {{ Math.round(day.temp?.max) }}° / {{ Math.round(day.temp?.min) }}°
                            </div>

                            <div class="forecast-uv">
                                UV {{ Math.round(day.uvi ?? 0) }}
                            </div>
                        </div>
                    </div>
                    <p v-else>Loading forecast...</p>
                </div>
            </div>
        </div>
    </div>

    <p class="update-time">
        Last updated: {{ lastUpdated }}
    </p>
</template>

<script setup>
import NavBar from '../components/NavBar.vue'
import { ref, computed, onMounted, onUnmounted } from 'vue'
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
const searchQuery = ref('')
const currentLocationMode = ref(true)
const dailyForecast = ref([])

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

async function searchLocation(query) {
    const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY
    const url = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(query)}&limit=1&appid=${apiKey}`

    const response = await fetch(url)

    if (!response.ok) {
        throw new Error('Failed to search location')
    }

    const data = await response.json()

    if (!data.length) {
        throw new Error('Location not found')
    }

    return {
        name: data[0].name,
        state: data[0].state || '',
        country: data[0].country || '',
        lat: data[0].lat,
        lon: data[0].lon
    }
}

async function loadWeatherAndUV(lat, lon, labelText) {
    const data = await fetchCurrentUV(lat, lon)

    latitude.value = lat
    longitude.value = lon
    locationStatus.value = labelText

    temperature.value = data.current?.temp != null ? Math.round(data.current.temp) : null
    humidity.value = data.current?.humidity ?? null
    icon.value = data.current?.weather?.[0]?.icon ?? ''
    windSpeed.value = data.current?.wind_speed ?? null
    timezone.value = data.timezone ?? ''
    weatherDesc.value = data.current?.weather?.[0]?.description ?? ''
    uvIndex.value = data.current?.uvi ?? null
    lastUpdated.value = new Date().toLocaleTimeString()
    dailyForecast.value = (data.daily || []).slice(0, 8)

    if (uvIndex.value === null) {
        throw new Error('UV index not found in API response')
    }
}

async function loadCurrentLocationData() {
    try {
        loading.value = true
        error.value = ''
        currentLocationMode.value = true
        locationStatus.value = 'Getting your current location...'

        const coords = await getUserLocation()
        await loadWeatherAndUV(
            coords.lat,
            coords.lon,
            'Showing current location weather'
        )
    } catch (err) {
        error.value = err.message || 'Something went wrong'
        locationStatus.value = 'Failed to get current location'
    } finally {
        loading.value = false
    }
}

async function handleSearch() {
    if (!searchQuery.value.trim()) {
        error.value = 'Please enter a city or suburb'
        return
    }

    try {
        loading.value = true
        error.value = ''
        currentLocationMode.value = false
        locationStatus.value = 'Searching location...'

        const location = await searchLocation(searchQuery.value.trim())

        const displayName = [
            location.name,
            location.state,
            location.country
        ]
            .filter(Boolean)
            .join(', ')

        await loadWeatherAndUV(
            location.lat,
            location.lon,
            `Showing weather for ${displayName}`
        )
    } catch (err) {
        error.value = err.message || 'Something went wrong'
        locationStatus.value = 'Failed to search location'
    } finally {
        loading.value = false
    }
}

let refreshTimer = null

onMounted(() => {
    loadCurrentLocationData()

    refreshTimer = setInterval(() => {
        if (currentLocationMode.value) {
            loadCurrentLocationData()
        } else if (latitude.value !== null && longitude.value !== null) {
            loadWeatherAndUV(
                latitude.value,
                longitude.value,
                locationStatus.value
            ).catch((err) => {
                error.value = err.message || 'Auto refresh failed'
            })
        }
    }, 600000)
})

onUnmounted(() => {
    if (refreshTimer) {
        clearInterval(refreshTimer)
    }
})


function getWeekday(timestamp) {
    return new Date(timestamp * 1000)
        .toLocaleDateString('en-AU', { weekday: 'short' })
}

function getDate(timestamp) {
    return new Date(timestamp * 1000)
        .toLocaleDateString('en-AU', {
            day: 'numeric',
            month: 'short'
        })
}
</script>

<style>
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px 32px;
    background: transparent;
}

.subtitle {
    color: #fefefe;
    margin-top: -10px;
    margin-bottom: 25px;
    font-size: 20px;
}

.search-bar {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 15px;
}

.search-bar input {
    flex: 1;
    min-width: 260px;
    padding: 12px 14px;
    border: 1px solid #ccc;
    border-radius: 10px;
    font-size: 14px;
}

.search-bar button {
    padding: 12px 16px;
    border: none;
    border-radius: 10px;
    background: #2c7be5;
    color: white;
    cursor: pointer;
    font-size: 14px;
}

.search-bar button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.location-label {
    margin-bottom: 20px;
    font-size: 20px;
    color: white;
}

.update-time {
    margin-top: 15px;
    font-size: 13px;
    color: #888;
    text-align: center;
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

.main-layout {
    display: grid;
    grid-template-columns: minmax(760px, 2fr) minmax(320px, 1.4fr);
    gap: 24px;
    margin-top: 20px;
    align-items: stretch;
}

.left-panel,
.right-panel {
    min-width: 0;
    align-self: stretch;
}

.left-panel {
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
}

.right-panel {
    display: flex;
    height: 100%;
}

.dashboard-row {
    display: grid;
    grid-template-columns: repeat(2, minmax(280px, 1fr));
    gap: 20px;
    align-items: stretch;
}

.dashboard-card {
    min-width: 0;
    height: 100%;
}

.future-card-placeholder {
    background: rgba(240, 240, 240, 0.75);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    color: #555;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    width: 100%;
    flex: 1;
    min-height: 100%;
    box-sizing: border-box;
    text-align: left;
}

.future-card-placeholder h3 {
    margin: 0 0 20px 0;
    font-size: 30px;
    font-weight: 700;
    color: #333;
    text-align: center;
}

.future-card-placeholder p {
    margin: 0;
    word-break: break-word;
    overflow-wrap: anywhere;
}

.left-panel,
.right-panel,
.dashboard-card {
    min-width: 0;
}

@media (max-width: 1100px) {
    .container {
        padding: 20px;
    }

    .main-layout {
        grid-template-columns: 1fr;
    }

    .right-panel {
        display: block;
    }

    .future-card-placeholder {
        height: auto;
        min-height: 260px;
    }
}

@media (max-width: 768px) {
    .container {
        padding: 16px;
    }

    h1 {
        font-size: 36px !important;
        line-height: 1.2;
    }

    .subtitle {
        margin-top: 0;
        margin-bottom: 20px;
        font-size: 14px;
    }

    .search-bar {
        flex-direction: column;
        align-items: stretch;
    }

    .search-bar input,
    .search-bar button {
        width: 100%;
    }

    .dashboard-row {
        grid-template-columns: 1fr;
    }

    .location-label,
    .update-time {
        font-size: 13px;
    }
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

/* Additional styles for forecast list */
.forecast-list {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 20px;
    width: 100%;
    margin-top: 0;
    flex: 1;
}

.forecast-item {
    display: grid;
    grid-template-columns: 70px 60px 1fr auto;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.55);
    color: #1f2d3d;
}

.forecast-day {
    font-weight: 600;
    display: flex;
    flex-direction: column;
    line-height: 1.1;
}

.weekday {
    font-size: 15px;
}

.date {
    font-size: 13px;
    color: #666;
}

.forecast-icon {
    width: 42px;
    height: 42px;
}

.forecast-temp {
    font-weight: 500;
}

.forecast-uv {
    font-size: 14px;
    font-weight: 600;
    color: #0F3D5E;
}

@media (max-width: 768px) {
    .forecast-item {
        grid-template-columns: 1fr auto;
        grid-template-areas:
            "day icon"
            "temp uv";
        row-gap: 6px;
    }

    .forecast-day {
        grid-area: day;
    }

    .forecast-icon {
        grid-area: icon;
        justify-self: end;
    }

    .forecast-temp {
        grid-area: temp;
    }

    .forecast-uv {
        grid-area: uv;
        justify-self: end;
    }
}
</style>