/**
 * Router configuration for SunSafe project.
 * Updated to handle User Story 2.2: Skin Analysis Tool.
 */
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // Setting SkinAnalysis as the primary view for Epic 2.0 testing
      path: '/',
      name: 'SkinAnalysis',
      // Using @ alias to ensure the path resolves correctly to src/views/
      component: () => import('@/views/SkinAnalysis.vue')
    }
  ]
})

export default router