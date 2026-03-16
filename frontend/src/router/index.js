import { createRouter, createWebHistory } from "vue-router"

// pages
import U1Dashboard from "../pages/U1Dashboard.vue"
import AustralianData from "../pages/AustralianData.vue"
import SkinAnalysis from "../pages/SkinAnalysis.vue"

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: U1Dashboard
  },
  {
    path: "/australian-data",
    name: "AustralianData",
    component: AustralianData
  },
  {
    path: "/skin-analysis",
    name: "SkinAnalysis",
    component: SkinAnalysis
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router