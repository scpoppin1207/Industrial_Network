<!-- components/ErrorOverlay.vue -->
<template>
  <transition name="fade-zoom">
    <div v-if="visible" class="error-overlay">
      <div class="error-content">
        ⚠️ {{ props.message }}
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps({
  message: String,
  errkey: Number
})



// 控制显示动画
const visible = ref(false)

watch(() => props.errkey, (errkey) => {
  if (errkey) {
    visible.value = true
    setTimeout(() => visible.value = false, 2000)
  }
})
</script>

<style scoped>
.error-overlay {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.error-content {
  font-size: 32px;
  font-weight: bold;
  color: #e53935;
  background: white;
  border: 4px solid #e53935;
  border-radius: 16px;
  padding: 24px 48px;
  box-shadow: 0 0 30px #e53935aa;
  animation: shake 0.3s ease-in-out infinite alternate;
}

/* 动画：轻微抖动 */
@keyframes shake {
  0%   { transform: rotate(-2deg); }
  100% { transform: rotate(2deg); }
}

/* 淡入+缩放动画 */
.fade-zoom-enter-active,
.fade-zoom-leave-active {
  transition: all 0.3s ease;
}
.fade-zoom-enter-from,
.fade-zoom-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>