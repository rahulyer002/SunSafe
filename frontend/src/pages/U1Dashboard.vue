<template>

    <div class="container">

        <h1>SunSafe Dashboard</h1>
        <WeatherCard />
        <UVCard />
        <ProtectionList />
        
    </div>

</template>

<script setup>

import WeatherCard from '../components/WeatherCard.vue'
import UVCard from '../components/UVCard.vue'
import ProtectionList from '../components/ProtectionList.vue'

</script>

<style>
.container {

    max-width: 400px;
    margin: auto;
    padding: 20px;

}
</style>