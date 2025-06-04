import { createRouter, createWebHistory } from 'vue-router'
import EntrySelector from '../components/EntrySelector.vue'
import SystemDesigner from '../components/SystemDesigner.vue'
import BlockDesigner from '../components/BlockDesigner.vue'

const routes = [
  { path: '/', component: EntrySelector },
  { path: '/system', component: SystemDesigner },
  { path: '/block', component: BlockDesigner }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router