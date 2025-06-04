<template>
  <div v-if="visible" class="dialog-mask">
    <div class="dialog-box">
      <div class="dialog-header">
        <div class="dialog-title">欢迎使用工业互联网智能搭建系统</div>
        <div class="dialog-subtitle">请输入您的需求，我们将为您智能生成流程</div>
      </div>
      
      <div class="dialog-content">
        <div class="input-container">
          <textarea 
            v-model="userInput" 
            rows="4" 
            placeholder="例如：我想要有三个货物仓库，分别储存鞋子、袜子、裤子。我想让我存鞋子的仓库运往4个目的地，都在一楼；袜子运往3个目的地，一个在1楼，两个在3楼；裤子就运往一个在2楼的目的地。"
            class="dialog-input"
          />
        </div>
        
        <div class="dialog-buttons">
          <button 
            @click="sendToBackend" 
            :disabled="loading" 
            class="dialog-button primary"
          >
            <span v-if="!loading">提交需求</span>
            <span v-else class="loading-spinner"></span>
          </button>
          
          <button 
            @click="closeDialog" 
            class="dialog-button secondary"
          >
            关闭
          </button>
        </div>
        
        <div v-if="loading" class="dialog-status">
          <div class="loading-indicator">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
          </div>
          <span>正在处理您的需求...</span>
        </div>
        
        <div v-if="response" class="dialog-response">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
            <path fill="#46c195" d="M9,16.17L4.83,12l-1.42,1.41L9,19L21,7l-1.41-1.41L9,16.17z"/>
          </svg>
          <span>{{ response }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: true }
})

const emit = defineEmits(['update:modelValue', 'flow-generated']) 

const visible = ref(props.modelValue)
const userInput = ref('')
const loading = ref(false)
const response = ref('')

const closeDialog = () => {
  visible.value = false
  emit('update:modelValue', false) 
}

const sendToBackend = async () => {
  loading.value = true
  response.value = ''
  try {
    // 假设后端接口为 /api/dialog
    const res = await fetch('/api/dialog', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: userInput.value })
    })
    const data = await res.json()
    response.value = data.reply // 这是LLM提取后的数组
    if (data.flow) {
      emit('flow-generated', data.flow) // 触发 flow-generated 事件
      closeDialog() // 发送成功后关闭对话框
    } else {
      response.value = '未生成流程，请检查输入或稍后再试。'
    }
  } catch (e) {
    response.value = '请求失败。'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.dialog-mask {
  position: fixed; 
  left: 0; 
  top: 0; 
  right: 0; 
  bottom: 0;
  background: rgba(15, 32, 39, 0.85); 
  z-index: 9999;
  display: flex; 
  align-items: center; 
  justify-content: center;
  backdrop-filter: blur(5px);
}

.dialog-box {
  background: rgba(25, 35, 45, 0.95);
  padding: 32px;
  border-radius: 16px;
  width: 600px;
  max-width: 90%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.dialog-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #1fa2ff, #46c195);
}

.dialog-header {
  margin-bottom: 24px;
  text-align: center;
}

.dialog-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
  background: linear-gradient(90deg, #1fa2ff, #46c195);
  -webkit-text-fill-color: transparent;
}

.dialog-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
}

.input-container {
  position: relative;
  margin-bottom: 24px;
}

.dialog-input {
  width: 100%;
  padding: 5px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  resize: vertical;
  min-height: 120px;
  transition: all 0.3s ease;
}

.dialog-input:focus {
  outline: none;
  border-color: #1fa2ff;
  box-shadow: 0 0 0 3px rgba(31, 162, 255, 0.2);
}

.dialog-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.input-decoration {
  position: absolute;
  bottom: 15px;
  right: 15px;
  opacity: 0.5;
}

.dialog-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.dialog-button {
  flex: 1;
  padding: 14px 20px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dialog-button.primary {
  background: linear-gradient(90deg, #1fa2ff, #46c195);
  color: white;
}

.dialog-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(31, 162, 255, 0.3);
}

.dialog-button.primary:disabled {
  background: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.dialog-button.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
}

.dialog-button.secondary:hover {
  background: rgba(255, 255, 255, 0.15);
}

.dialog-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
  padding: 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
}

.loading-indicator {
  display: flex;
  gap: 6px;
}

.loading-dot {
  width: 8px;
  height: 8px;
  background: #1fa2ff;
  border-radius: 50%;
  animation: pulse 1.4s infinite ease-in-out;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 1;
  }
  30% {
    transform: translateY(-6px);
    opacity: 0.7;
  }
}

.dialog-response {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #46c195;
  font-size: 0.95rem;
  padding: 12px;
  border-radius: 8px;
  background: rgba(70, 193, 149, 0.1);
  margin-top: 16px;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>