<template>

<div class="page">

<h2>Skin Cancer Incidence in Australia</h2>

<div class="filters">

<label>Start Year</label>
<select v-model.number="startYear" @change="updateChart">
<option v-for="y in years" :key="y" :value="y">
  {{y}}
</option>
</select>

<label>End Year</label>
<select v-model.number="endYear" @change="updateChart">
<option v-for="y in years" :key="y" :value="y">
  {{y}}
</option>
</select>

<label>City</label>
<select v-model="city" @change="updateChart">
<option value="Melbourne">Melbourne</option>
</select>

</div>

<canvas ref="chartCanvas"></canvas>

</div>

</template>

<script>

import { Chart } from "chart.js/auto"

export default {

data(){

return{

chart:null,

startYear:2000,
endYear:2020,
city:"Melbourne",

years:[2000,2005,2010,2015,2020],

dataSet:[
{year:2000, incidence_rate:50, city:"Melbourne"},
{year:2005, incidence_rate:55, city:"Melbourne"},
{year:2010, incidence_rate:65, city:"Melbourne"},
{year:2015, incidence_rate:75, city:"Melbourne"},
{year:2020, incidence_rate:85, city:"Melbourne"}
]

}

},

mounted(){

this.createChart()

},

methods:{

getFilteredData(){

return this.dataSet.filter(d =>

d.year >= this.startYear &&
d.year <= this.endYear &&
d.city === this.city

)

},

createChart(){

const ctx = this.$refs.chartCanvas.getContext("2d")

const filtered = this.getFilteredData()

this.chart = new Chart(ctx,{

type:"line",

data:{

labels: filtered.map(d => d.year),

datasets:[{

label:"Cases per 100,000",

data: filtered.map(d => d.incidence_rate),

borderColor:"green",

backgroundColor:"rgba(0,150,0,0.2)",

tension:0.3,

fill:true

}]

},

options:{
responsive:true,
maintainAspectRatio:false
}

})

},

updateChart(){

if(!this.chart) return

const filtered = this.getFilteredData()

this.chart.data.labels = filtered.map(d => d.year)

this.chart.data.datasets[0].data = filtered.map(d => d.incidence_rate)

this.chart.update()

}

}

}

</script>

<style>

.page{
width:700px;
margin:auto;
margin-top:40px;
text-align:center;
}

.filters{
margin-bottom:20px;
display:flex;
gap:15px;
justify-content:center;
align-items:center;
}

select{
padding:5px;
}

canvas{
margin-top:20px;
height:400px;
}

</style>