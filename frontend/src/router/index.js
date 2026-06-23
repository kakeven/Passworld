import { createRouter, createWebHashHistory } from 'vue-router'
import Login_view from '@/views/Login_view.vue'
import Vault_view from '@/views/Vault_view.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: Login_view },
    { path: '/vault', component: Vault_view }
  ]
})

export default router