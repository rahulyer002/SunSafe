<template>
  <nav class="navbar">

    <div class="logo">
      ☀️ SunSafe
    </div>

    <div class="nav-links">

      <router-link to="/" class="nav-item">
        Dashboard
      </router-link>

      <router-link to="/australian-data" class="nav-item">
        Australian Data
      </router-link>

      <router-link to="/skin-analysis" class="nav-item">
        Skin Analysis
      </router-link>

    </div>

  </nav>
</template>

<style scoped>

.navbar{
    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:18px 32px;

    background:rgba(0,0,0,0.25);

    backdrop-filter: blur(12px);

    border-radius:18px;

    margin-bottom:20px;
}

.logo{
    font-size:30px;
    font-weight:700;
    color:white;
}

.nav-links{
    display:flex;
    gap:40px;
}

.nav-item{
    color:white;
    text-decoration:none;

    font-size:25px;

    transition:0.25s;
}

.nav-item:hover{
    opacity:0.7;
}

.router-link-active{
    border-bottom:2px solid white;
    padding-bottom:4px;
}

</style>