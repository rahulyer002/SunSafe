<template>
  <router-view />
</template>

<style>
/* Global Resets */
body, html, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #0f172a; /* Match the dark theme */
}

/* Ensure smooth font rendering */
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>