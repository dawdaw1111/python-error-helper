import { createRouter, createWebHistory } from 'vue-router'

import { ensureAuthInitialized, isAuthenticated } from '../auth'
import AdminView from '../views/AdminView.vue'
import AnalyzeView from '../views/AnalyzeView.vue'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/analyze', name: 'analyze', component: AnalyzeView },
    { path: '/search', name: 'search', component: SearchView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/admin', name: 'admin', component: AdminView, meta: { requiresAuth: true } },
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach(async (to) => {
  await ensureAuthInitialized()

  if (to.meta.requiresAuth && !isAuthenticated()) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }
  }

  if (to.name === 'login' && isAuthenticated()) {
    return { name: 'admin' }
  }

  return true
})

export default router
