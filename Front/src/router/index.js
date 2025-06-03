import { createRouter, createWebHistory } from 'vue-router'
import EntrySelector from '../components/EntrySelector.vue'
import SystemDesigner from '../components/SystemDesigner.vue'

const routes = [
  { path: '/', component: EntrySelector },
  { path: '/system', component: SystemDesigner },
  { path: '/custom', component: { template: '<div style="margin:auto;font-size:2em;">自定义模块开发中...</div>' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router