import { createRouter, createWebHistory } from "vue-router"

// loading pages
import U1Dashboard from "../pages/U1Dashboard.vue"
import AustralianData from "../pages/AustralianData.vue"

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router