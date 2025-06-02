<template>
  <div v-if="visible" class="dialog-mask">
    <div class="dialog-box">
      <div class="dialog-title">欢迎使用工业互联网智能搭建系统，请输入你的需求。</div>
      <textarea v-model="userInput" rows="4" style="width:100%;margin-bottom:10px;" />
      <div>
        <button @click="sendToBackend" :disabled="loading">提交</button>
        <button @click="closeDialog" style="margin-left:8px;">关闭</button>
      </div>
      <div v-if="loading" style="margin-top:8px;">正在提交...</div> 
      <div v-if="response" style="margin-top:8px;color:green;">{{ response }}</div>
    </div>
  </div>
</template>

<!-- <script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: true }
})
const emit = defineEmits(['update:modelValue']) 

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
    // response.value = data.flow // 这是来自后端的json文件

    // setTimeout(closeDialog, 2000) // 2秒后自动关闭
  } catch (e) {
    response.value = '请求失败'
  } finally {
    loading.value = false
  }
}
</script> -->

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

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
  position: fixed; left: 0; top: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.2); z-index: 9999;
  display: flex; align-items: center; justify-content: center;
}
.dialog-box {
  background: #fff; padding: 24px; border-radius: 8px; min-width: 320px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.dialog-title {
  font-weight: bold; margin-bottom: 12px;
}
</style>