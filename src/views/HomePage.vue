<template>

<div class="home">

<h1>UV Protection App</h1>

<p>Check Australian UV Data</p>

<button @click="goData">
View Australian Data
</button>

</div>

</template>

<script>

export default{

methods:{

goData(){

this.$router.push("/data")

}

}

}

</script>

<style>

.home{
text-align:center;
margin-top:100px;
}

button{
padding:10px 20px;
font-size:18px;
}

</style>