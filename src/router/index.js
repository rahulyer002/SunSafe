import { createRouter, createWebHistory } from "vue-router"

import HomePage from "../views/HomePage.vue"
import AustralianData from "../views/AustralianData.vue"

const routes = [

{
path: "/",
component: HomePage
},

{
path: "/data",
component: AustralianData
}

]

const router = createRouter({

history: createWebHistory(),
routes

})

export default router