import { createApp } from 'vue'
import App from './App.vue'

// ✅ 确保这两行样式导入
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

createApp(App).mount('#app')