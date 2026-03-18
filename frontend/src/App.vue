<template>
  <div>

    <nav style="padding:20px;">
      <router-link to="/">Dashboard</router-link> |
      <router-link to="/australian-data">Australian Data</router-link> |
      <router-link to="/skin-analysis">Skin Analysis</router-link>
    </nav>

    <router-view />

  </div>
</template>

<script setup>
</script>

<style>
body {
    background-color: #173449;
    margin: 0;
}</style>