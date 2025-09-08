import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'

import App from './App.vue'
import LoginView from './views/LoginView.vue'

// Import des styles
import './styles/neumorphic.css'

// Configuration du routeur
const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/feed',
    name: 'Feed',
    component: () => import('./views/FeedView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navigation pour l'authentification
router.beforeEach(async (to, from, next) => {
  try {
    // Essayer d'importer les APIs
    const { default: odooApi } = await import('./services/odooApi.js')
    const { default: demoApi } = await import('./services/demoApi.js')
    
    if (to.meta.requiresAuth) {
      const isAuthenticated = odooApi.isAuthenticated() || demoApi.isAuthenticated()
      if (!isAuthenticated) {
        next('/login')
        return
      }
    }
    next()
  } catch (error) {
    console.error('Erreur dans le guard de navigation:', error)
    // En cas d'erreur, rediriger vers login
    if (to.meta.requiresAuth) {
      next('/login')
    } else {
      next()
    }
  }
})

// Création de l'application
const app = createApp(App)

app.use(router)
app.use(createPinia())

app.mount('#app')