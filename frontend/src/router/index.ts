import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import PluginLoader from '@/components/PluginLoader.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/plugin/:id',
      name: 'plugin',
      component: PluginLoader,
      props: true
    }
  ]
})

export default router

