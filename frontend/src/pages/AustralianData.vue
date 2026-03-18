<template>
    <div>
        <NavBar />
    </div>
<div class="page">

<!-- Skin Cancer Chart -->
<h2>Skin Cancer Incidence in Australia</h2>

<div class="filters">

<label>Start Year</label>
<select v-model.number="cancerStartYear" @change="renderCancerChart">
<option v-for="y in cancerYears" :key="y" :value="y">{{y}}</option>
</select>

<label>End Year</label>
<select v-model.number="cancerEndYear" @change="renderCancerChart">
<option v-for="y in cancerYears" :key="y" :value="y">{{y}}</option>
</select>

<label>City</label>
<select v-model="cancerCity" @change="renderCancerChart">
<option value="Melbourne">Melbourne</option>
</select>

</div>

<div class="chart-container">
<canvas ref="cancerChart"></canvas>
</div>


<!-- UV Chart -->
<h2>Trend of Heat in Australia</h2>

<div class="filters">

<label>Start Year</label>
<select v-model.number="uvStartYear" @change="renderUVChart">
<option v-for="y in uvYears" :key="y" :value="y">{{y}}</option>
</select>

<label>End Year</label>
<select v-model.number="uvEndYear" @change="renderUVChart">
<option v-for="y in uvYears" :key="y" :value="y">{{y}}</option>
</select>

<label>City</label>
<select v-model="uvCity" @change="renderUVChart">
<option value="Melbourne">Melbourne</option>
</select>

</div>

<div class="chart-container">
<canvas ref="uvChart"></canvas>
</div>

</div>

</template>


<script>


import { Chart } from "chart.js/auto"

let cancerChart = null
let uvChart = null

export default {

data(){
return{

// cancer filter
cancerStartYear:null,
cancerEndYear:null,
cancerCity:"Melbourne",

// uv filter
uvStartYear:null,
uvEndYear:null,
uvCity:"Melbourne",

// data
cancerData:[],
uvData:[],

// years
cancerYears:[],
uvYears:[]

}
},

mounted(){
this.fetchData()
},

methods:{

async fetchData(){

const cancerRes = await fetch("https://sunsafe-zku7.onrender.com/cancer/")
const cancer = await cancerRes.json()

const uvRes = await fetch("https://sunsafe-zku7.onrender.com/uv/")
const uv = await uvRes.json()

this.cancerData = cancer.map(d=>({
year:Number(d.year),
incidence_rate:Number(d.incidence_rate),
city:d.city
}))

this.uvData = uv.map(d=>({
year:Number(d.year),
uv_index:Number(d.uv_index),
city:d.city
}))

this.cancerYears = [...new Set(this.cancerData.map(d=>d.year))].sort((a,b)=>a-b)
this.uvYears = [...new Set(this.uvData.map(d=>d.year))].sort((a,b)=>a-b)

this.cancerStartYear = this.cancerYears[0]
this.cancerEndYear = this.cancerYears[this.cancerYears.length-1]

this.uvStartYear = this.uvYears[0]
this.uvEndYear = this.uvYears[this.uvYears.length-1]

this.$nextTick(()=>{
this.renderCancerChart()
this.renderUVChart()
})

},

getCancerFiltered(){

return this.cancerData
.filter(d =>
d.year >= this.cancerStartYear &&
d.year <= this.cancerEndYear &&
d.city === this.cancerCity
)
.sort((a,b)=>a.year-b.year)

},

getUVFiltered(){

return this.uvData
.filter(d =>
d.year >= this.uvStartYear &&
d.year <= this.uvEndYear &&
d.city === this.uvCity
)
.sort((a,b)=>a.year-b.year)

},

renderCancerChart(){

if(!this.$refs.cancerChart) return

const ctx = this.$refs.cancerChart.getContext("2d")

const data = this.getCancerFiltered()

if(cancerChart){
cancerChart.destroy()
}

cancerChart = new Chart(ctx,{

type:"line",

data:{
labels:data.map(d=>d.year),
datasets:[{
label:"Cases per 100,000",
data:data.map(d=>d.incidence_rate),
borderColor:"#0a7f2e",
backgroundColor:"rgba(10,127,46,0.2)",
tension:0.3,
fill:true
}]
},

options:{responsive:true,maintainAspectRatio:false}

})

},

renderUVChart(){

if(!this.$refs.uvChart) return

const ctx = this.$refs.uvChart.getContext("2d")

const data = this.getUVFiltered()

if(uvChart){
uvChart.destroy()
}

uvChart = new Chart(ctx,{

type:"line",

data:{
labels:data.map(d=>d.year),
datasets:[{
label:"UV Index",
data:data.map(d=>d.uv_index),
borderColor:"#ff7b00",
backgroundColor:"rgba(255,123,0,0.2)",
tension:0.3,
fill:true
}]
},

options:{responsive:true,maintainAspectRatio:false}

})

}

}

}

</script>

<script setup>
import NavBar from '../components/NavBar.vue'
</script>

<style>

.page{
width:900px;
margin:auto;
margin-top:40px;
text-align:center;
}

.filters{
margin-bottom:20px;
display:flex;
gap:20px;
justify-content:center;
}

.chart-container{
width:900px;
height:420px;
margin-bottom:50px;
}

</style>