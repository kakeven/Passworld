import { createRouter, createWebHistory } from 'vue-router'
import Login_view from '@/views/Login_view.vue'
import Vault_view from '@/views/Vault_view.vue'

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    { path: '/', component: Login_view },
    { path: '/vault', component: Vault_view }
  ],
})

export default router