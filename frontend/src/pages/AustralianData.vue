<template>
<div>
  <!-- top navigation bar -->
  <NavBar />
</div>

<div class="page">

<!-- loading state -->
<div v-if="loading" class="loading">
  Loading data...
</div>

<div v-else>

<!-- Cancer Chart -->
<h2>Skin Cancer Incidence in Australia</h2>

<div class="filters">

<!-- start year filter -->
<div class="filter-item">
<label>Start Year</label>
<select v-model.number="cancerStartYear">
<option v-for="y in cancerYears" :key="y" :value="y">{{y}}</option>
</select>
</div>

<!-- end year filter -->
<div class="filter-item">
<label>End Year</label>
<select v-model.number="cancerEndYear">
<option v-for="y in cancerYears" :key="y" :value="y">{{y}}</option>
</select>
</div>

<!-- city filter -->
<div class="filter-item">
<label>City</label>
<select v-model="cancerCity">
<option value="Melbourne">Melbourne</option>
</select>
</div>

</div>

<div class="chart-container">

<!-- show error if year range is wrong -->
<div v-if="cancerStartYear > cancerEndYear" class="error">
End year must be greater than or equal to start year
</div>

<!-- chart canvas -->
<canvas v-else ref="cancerChart"></canvas>

</div>


<!-- UV Chart -->
<h2>Trend of Heat in Australia</h2>

<div class="filters">

<!-- start year filter -->
<div class="filter-item">
<label>Start Year</label>
<select v-model.number="uvStartYear">
<option v-for="y in uvYears" :key="y" :value="y">{{y}}</option>
</select>
</div>

<!-- end year filter -->
<div class="filter-item">
<label>End Year</label>
<select v-model.number="uvEndYear">
<option v-for="y in uvYears" :key="y" :value="y">{{y}}</option>
</select>
</div>

<!-- city filter -->
<div class="filter-item">
<label>City</label>
<select v-model="uvCity">
<option value="Melbourne">Melbourne</option>
</select>
</div>

</div>

<div class="chart-container">

<!-- show error if year range is wrong -->
<div v-if="uvStartYear > uvEndYear" class="error">
End year must be greater than or equal to start year
</div>

<!-- show chart -->
<canvas v-else ref="uvChart"></canvas>

</div>

</div>
</div>
</template>

<script>
import { Chart } from "chart.js/auto"
import NavBar from '../components/NavBar.vue'

export default {

components:{ NavBar },

data(){
return{

loading:true, // loading boolean

// filters 
cancerStartYear:null,
cancerEndYear:null,
cancerCity:"Melbourne",

uvStartYear:null,
uvEndYear:null,
uvCity:"Melbourne",


cancerData:[],
uvData:[],

cancerYears:[],
uvYears:[],

cancerChart:null,
uvChart:null

}
},

mounted(){
this.fetchData()
},

watch:{

// when cancer data changes → re-render chart
cancerData(){
this.$nextTick(()=>{ this.renderCancerChart() })
},

uvData(){
this.$nextTick(()=>{ this.renderUVChart() })
},

cancerStartYear(){ this.renderCancerChart() },
cancerEndYear(){ this.renderCancerChart() },
cancerCity(){ this.renderCancerChart() },

uvStartYear(){ this.renderUVChart() },
uvEndYear(){ this.renderUVChart() },
uvCity(){ this.renderUVChart() }

},

methods:{

// API
async fetchData(){

this.loading = true

try{

// get cancer data
const cancerRes = await fetch("https://sunsafe-zku7.onrender.com/cancer/")
const cancer = await cancerRes.json()

// get UV data
const uvRes = await fetch("https://sunsafe-zku7.onrender.com/uv/")
const uv = await uvRes.json()

// format cancer data
this.cancerData = cancer.map(d=>({
year:Number(d.year),
incidence_rate:Number(d.incidence_rate),
city:d.city
}))

// format UV data
this.uvData = uv.map(d=>({
year:Number(d.year),
uv_index:Number(d.uv_index),
city:d.city
}))

// get all years
this.cancerYears = [...new Set(this.cancerData.map(d=>d.year))].sort((a,b)=>a-b)
this.uvYears = [...new Set(this.uvData.map(d=>d.year))].sort((a,b)=>a-b)

// set default start - end years
this.cancerStartYear = this.cancerYears[0] ?? null
this.cancerEndYear = this.cancerYears[this.cancerYears.length-1] ?? null

this.uvStartYear = this.uvYears[0] ?? null
this.uvEndYear = this.uvYears[this.uvYears.length-1] ?? null

}catch(err){
console.error(err)
}finally{
this.loading = false
}

},

// filter cancer data based on selected values
getCancerFiltered(){
return this.cancerData
.filter(d =>
d.year >= (this.cancerStartYear ?? -Infinity) &&
d.year <= (this.cancerEndYear ?? Infinity) &&
d.city === this.cancerCity
)
.sort((a,b)=>a.year-b.year)
},

// filter UV data
getUVFiltered(){
return this.uvData
.filter(d =>
d.year >= (this.uvStartYear ?? -Infinity) &&
d.year <= (this.uvEndYear ?? Infinity) &&
d.city === this.uvCity
)
.sort((a,b)=>a.year-b.year)
},

// draw cancer chart
renderCancerChart(){

// stop if invalid range
if(this.cancerStartYear > this.cancerEndYear) return
if(!this.$refs.cancerChart) return

const ctx = this.$refs.cancerChart.getContext("2d")
const data = this.getCancerFiltered()

// destroy old chart
if(this.cancerChart){
this.cancerChart.destroy()
}

// create new chart
this.cancerChart = new Chart(ctx,{
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

// draw UV chart
renderUVChart(){

if(this.uvStartYear > this.uvEndYear) return
if(!this.$refs.uvChart) return

const ctx = this.$refs.uvChart.getContext("2d")
const data = this.getUVFiltered()

if(this.uvChart){
this.uvChart.destroy()
}

this.uvChart = new Chart(ctx,{
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

<style>

.page{
max-width:900px;
width:90%;
margin:auto;
margin-top:40px;
text-align:center;
}

.loading{
font-size:20px;
margin-top:50px;
}

.filters{
margin-bottom:20px;
display:flex;
gap:15px;
justify-content:center;
flex-wrap:wrap;
}

.filter-item{
display:flex;
align-items:center;
gap:6px;
}

select{
padding:10px 14px;
font-size:16px;
border-radius:6px;
border:1px solid #ccc;
min-width:120px;
}

.chart-container{
width:100%;
height:350px;
margin-bottom:40px;
}

.error{
color:#ff4d4f;
font-size:16px;
margin-top:20px;
font-weight:500;
}

@media (max-width:600px){

.chart-container{
height:250px;
}

.filters{
flex-direction:column;
align-items:center;
}

select{
width:100%;
}

}

</style>