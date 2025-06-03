<template>
  <div class="entry-selector">
    <div class="background-animation"></div>
    <h2>请选择入口</h2>
    <p class="subtitle">选择一个模块开始您的体验</p>
    
    <div class="buttons-container">
      <div 
        class="entry-card" 
        @click="select('custom')"
        :class="{'hover-effect': hoverState === 'custom'}"
        @mouseenter="hoverState = 'custom'"
        @mouseleave="hoverState = null"
      >
        <div class="icon-container">
          <div class="icon-bg">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 4H8c-1.4 0-2.5 1.1-2.5 2.5v11c0 1.4 1.1 2.5 2.5 2.5h8c1.4 0 2.5-1.1 2.5-2.5v-11c0-1.4-1.1-2.5-2.5-2.5Z"/>
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18 6.5c0-1.4-1.1-2.5-2.5-2.5h-7c-1.4 0-2.5 1.1-2.5 2.5v11c0 1.4 1.1 2.5 2.5 2.5h7c1.4 0 2.5-1.1 2.5-2.5v-11Z"/>
            </svg>
          </div>
        </div>
        <h3>自定义模块</h3>
        <p>创建并配置个性化功能</p>
        <div class="enter-btn">开始使用</div>
      </div>
      
      <div 
        class="entry-card" 
        @click="select('system')"
        :class="{'hover-effect': hoverState === 'system'}"
        @mouseenter="hoverState = 'system'"
        @mouseleave="hoverState = null"
      >
        <div class="icon-container">
          <div class="icon-bg">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 6h6M9 12h6M9 18h6"/>
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.8 21.5h14.4c1.3 0 2.3-1 2.3-2.3V4.8c0-1.3-1-2.3-2.3-2.3H4.8C3.5 2.5 2.5 3.5 2.5 4.8v14.4c0 1.3 1 2.3 2.3 2.3Z"/>
            </svg>
          </div>
        </div>
        <h3>系统设计</h3>
        <p>设计系统整体架构和流程</p>
        <div class="enter-btn">开始使用</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const hoverState = ref(null)

function select(type) {
  if (type === 'system') router.push('/system')
  else if (type === 'custom') router.push('/custom')
}
</script>

<style scoped>
.entry-selector {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  position: relative;
  overflow: hidden;
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(41, 128, 185, 0.1) 0%, transparent 25%),
    radial-gradient(circle at 90% 80%, rgba(46, 204, 113, 0.1) 0%, transparent 25%);
  z-index: 0;
  animation: gradientShift 15s ease infinite;
}

h2 {
  font-size: 2.8rem;
  color: #ffffff;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 2;
  position: relative;
}

h2::after {
  content: '';
  display: block;
  width: 80px;
  height: 4px;
  background: linear-gradient(to right, #1fa2ff, #12d8fa, #a6ffcb);
  margin: 15px auto 30px;
  border-radius: 2px;
}

.subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.2rem;
  margin-bottom: 40px;
  z-index: 2;
}

.buttons-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  z-index: 2;
}

.entry-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  width: 280px;
  padding: 35px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.entry-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #1fa2ff, #a6ffcb);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.hover-effect::before {
  opacity: 1;
}

.entry-card:hover {
  transform: translateY(-10px) scale(1.02);
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
}

.icon-container {
  margin-bottom: 25px;
}

.icon-bg {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(31, 162, 255, 0.15), rgba(166, 255, 203, 0.15));
}

.icon-bg svg {
  width: 40px;
  height: 40px;
  stroke: #1fa2ff;
}

.entry-card:nth-child(2) .icon-bg {
  background: linear-gradient(135deg, rgba(86, 67, 253, 0.15), rgba(151, 60, 255, 0.15));
}

.entry-card:nth-child(2) .icon-bg svg {
  stroke: #8643ff;
}

h3 {
  font-size: 1.5rem;
  color: white;
  margin-bottom: 12px;
}

.entry-card p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin-bottom: 25px;
  line-height: 1.6;
}

.enter-btn {
  display: inline-block;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.9);
  border-radius: 50px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.entry-card:hover .enter-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-3px);
}

@keyframes gradientShift {
  0% {
    background-position: 0% 0%;
  }
  50% {
    background-position: 100% 100%;
  }
  100% {
    background-position: 0% 0%;
  }
}

@media (max-width: 768px) {
  .buttons-container {
    flex-direction: column;
    gap: 30px;
  }
  
  .entry-selector {
    padding: 20px;
  }
  
  h2 {
    font-size: 2.2rem;
    text-align: center;
  }
}
</style>