<template>
  <div class="design-page-wrapper">
    <div class="module-design-container">
      <div class="design-header">
        <h1>模块设计界面</h1>
        <p>输入您的模块需求，系统将智能生成设计方案</p>
      </div>
      
      <div class="design-layout">
        <!-- 左侧输入/结果区域 -->
        <div class="design-main">
          <div class="input-section">
            <div class="input-container">
              <textarea 
                v-model="userInput" 
                placeholder="例如：我需要一个分拣装置，驱动事件就是有物品到达，执行动作是分拣物品到指定位置，结束条件是物品被分拣完毕。"
                class="design-input"
              ></textarea>
            </div>
            
            <div class="button-group">
              <button 
                @click="submitDesignRequest" 
                :disabled="loading" 
                class="submit-button"
              >
                <span v-if="!loading">生成设计方案</span>
                <span v-else class="loading-spinner"></span>
              </button>
              
              <button 
                v-if="designResult" 
                @click="saveModule" 
                class="add-module-button"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
                  <path fill="currentColor" d="M19,13h-6v6h-2v-6H5v-2h6V5h2v6h6V13z"/>
                </svg>
                保存当前模块并继续添加自定义模块
              </button>
            </div>
          </div>
          
          <div class="result-section">
            <div v-if="loading" class="loading-indicator">
              <div class="loading-dot"></div>
              <div class="loading-dot"></div>
              <div class="loading-dot"></div>
              <span>正在生成设计方案...</span>
            </div>
            
            <div v-if="error" class="error-message">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                <path fill="#ff6b6b" d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10s10-4.48,10-10S17.52,2,12,2z M13,17h-2v-2h2V17z M13,13h-2V7h2V13z"/>
              </svg>
              <span>{{ error }}</span>
            </div>
            
            <div v-if="designResult" class="design-result">
              <div class="result-header">
                <h2>设计方案</h2>
                <div class="result-meta">
                  <span>生成时间: {{ new Date().toLocaleString() }}</span>
                  <button @click="copyToClipboard" class="copy-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
                      <path fill="#1fa2ff" d="M16,1H4C2.9,1,2,1.9,2,3v16h2V3h12V1z M19,5H8C6.9,5,6,5.9,6,7v14c0,1.1,0.9,2,2,2h11c1.1,0,2-0.9,2-2V7C21,5.9,20.1,5,19,5z M19,21H8V7h11V21z"/>
                    </svg>
                    复制
                  </button>
                </div>
              </div>
              
              <div class="result-content">
                <pre>{{ designResult }}</pre>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 右侧模块库 -->
        <div class="module-library">
          <div class="library-header">
            <h2>自定义模块库</h2>
            <div class="module-count">{{ savedModules.length }} 个模块</div>
          </div>


          <div class="library-actions">

            <button @click="goToSystem" class="system-button">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
                <path fill="currentColor" d="M4,18h16c1.1,0,2-0.9,2-2V6c0-1.1-0.9-2-2-2H4C2.9,4,2,4.9,2,6v10C2,17.1,2.9,18,4,18z M4,6h16v10H4V6z M11,9 l-3.2,3.2l-1.4-1.4L4,13l4.6,4.6L15,10.4L11,9z"/>
              </svg>
              进入系统设计
            </button>
            
            <button 
              v-if="savedModules.length > 0" 
              @click="clearModules" 
              class="clear-button"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
                <path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
              </svg>
              清空模块库
            </button>
          </div>

          <div class="module-list">
            <div v-if="savedModules.length === 0" class="empty-library">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="48" height="48">
                <path fill="#1fa2ff" d="M19,5v14H5V5H19 M19,3H5C3.9,3,3,3.9,3,5v14c0,1.1,0.9,2,2,2h14c1.1,0,2-0.9,2-2V5C21,3.9,20.1,3,19,3z M12,6c-1.66,0-3,1.34-3,3s1.34,3,3,3s3-1.34,3-3S13.66,6,12,6z M18,15.58C18,13.08,14.97,12,12,12s-6,1.08-6,3.58V17h12V15.58z"/>
              </svg>
              <p>暂无已保存模块</p>
              <p>生成并保存第一个模块</p>
            </div>
            
            <div 
              v-for="(module, index) in savedModules" 
              :key="index" 
              class="module-item"
            >
              <div class="module-info">
                <div class="module-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                    <path fill="#46c195" d="M20,6h-8l-2-2H4C2.9,4,2.01,4.9,2.01,6L2,18c0,1.1,0.9,2,2,2h16c1.1,0,2-0.9,2-2V8C22,6.9,21.1,6,20,6z M14,16H8v-2h6V16z M16,11H8V9h8V11z"/>
                  </svg>
                </div>
                <div class="module-content">
                  <h3>{{ module.name || `自定义模块 ${index + 1}` }}</h3>
                  <div class="module-preview">{{ truncateContent(module.content) }}</div>
                </div>
              </div>
              <div class="module-actions">
                <button @click="viewModule(module)" class="action-button view">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
                    <path fill="#1fa2ff" d="M12,6.5c3.79,0,7.17,2.13,8.82,5.5c-1.65,3.37-5.02,5.5-8.82,5.5S4.83,15.37,3.18,12C4.83,8.63,8.21,6.5,12,6.5 M12,4.5 C7,4.5,2.73,7.61,1,12c1.73,4.39,6,7.5,11,7.5s9.27-3.11,11-7.5C21.27,7.61,17,4.5,12,4.5L12,4.5z"/>
                    <path fill="#1fa2ff" d="M12,9c1.66,0,3,1.34,3,3s-1.34,3-3,3s-3-1.34-3-3S10.34,9,12,9 M12,7c-2.76,0-5,2.24-5,5s2.24,5,5,5s5-2.24,5-5 S14.76,7,12,7L12,7z"/>
                  </svg>
                  查看
                </button>
                <button 
                  v-if="module.xmlfbt" 
                  @click="downloadFBT(module)" 
                  class="action-button download-fbt"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
                  </svg>
                  下载FBT
                </button>
                <button @click="deleteModule(index)" class="action-button delete">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16">
                    <path fill="#ff6b6b" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                  </svg>
                  删除
                </button>
              </div>
              <div class="module-time">{{ module.timestamp }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// 模块设计相关状态
const userInput = ref('')
const loading = ref(false)
const designResult = ref('') // Stores the JSON design
const generatedXmlFbt = ref('') // Stores the FBT XML string for the current design
const error = ref('')

// 模块库相关状态
const savedModules = ref([])

onMounted(() => {
  // 尝试从 localStorage 加载已保存的模块
  const saved = localStorage.getItem('savedModules')
  if (saved) {
    try {
      savedModules.value = JSON.parse(saved)
    } catch (e) {
      console.error('解析保存的模块出错:', e)
      savedModules.value = []
    }
  }
})
const router = useRouter()

const goToSystem = () => {
  router.push('../system')
}
const submitDesignRequest = async () => {
  if (!userInput.value.trim()) {
    error.value = '请输入设计需求'
    return
  }
  
  loading.value = true
  error.value = ''
  designResult.value = ''
  generatedXmlFbt.value = '' // Reset FBT content
  
  try {
    const response = await fetch('/api/module-design', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: userInput.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`请求失败: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('服务器返回数据:', data)
   
    designResult.value = data.design // JSON design
    if (data.xmlfbt) {
      generatedXmlFbt.value = data.xmlfbt // FBT XML string
    }
  } catch (err) {
    error.value = `请求失败: ${err.message}`
    console.error('模块设计请求失败:', err)
  } finally {
    loading.value = false
  }
}

// 保存当前模块到模块库
const saveModule = () => {
  if (!designResult.value) return
  console.log('保存模块:', designResult.value.name)
  const newModule = {
    id: Date.now(),
    name: designResult.value.name,
    content: designResult.value, // JSON content
    xmlfbt: generatedXmlFbt.value, // FBT XML string
    timestamp: new Date().toLocaleString(),
    userInput: userInput.value
  }
  
  savedModules.value.unshift(newModule)
  saveModulesToStorage()
  
  // 清空当前输入和结果
  userInput.value = ''
  designResult.value = ''
  generatedXmlFbt.value = '' // Clear FBT content as well
  error.value = ''
}

// 保存模块到本地存储
const saveModulesToStorage = () => {
  localStorage.setItem('savedModules', JSON.stringify(savedModules.value))
}

// 删除模块
const deleteModule = (index) => {
  savedModules.value.splice(index, 1)
  saveModulesToStorage()
}

// 查看模块详情
const viewModule = (module) => {
  userInput.value = module.userInput
  designResult.value = module.content // module.content is the JSON
  generatedXmlFbt.value = module.xmlfbt || '' // Populate FBT for the viewed module
  // 滚动到顶部
  document.querySelector('.design-page-wrapper').scrollTo(0, 0)
}

// 截取模块内容用于预览
const truncateContent = (content) => {
  const description = content.des || JSON.stringify(content)
  return description.length > 100 
    ? description.substring(0, 100) + '...'
    : description
}

// 新增：下载FBT文件的方法
const downloadFBT = (module) => {
  if (!module.xmlfbt) {
    alert('此模块没有可下载的FBT内容。')
    return
  }

  const fbtContent = module.xmlfbt
  const moduleName = (module.name || 'custom_module').replace(/\s+/g, '_')
  const filename = `${moduleName}.fbt`

  const blob = new Blob([fbtContent], { type: 'application/xml;charset=utf-8' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = filename
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(link.href)
  
  showNotification(`已开始下载 ${filename}`, 'success')
}

const copyToClipboard = () => {
  if (designResult.value) {
    // Assuming designResult is an object, stringify it for copying
    const textToCopy = typeof designResult.value === 'string' 
      ? designResult.value 
      : JSON.stringify(designResult.value, null, 2);
    navigator.clipboard.writeText(textToCopy)
      .then(() => {
        alert('设计方案已复制到剪贴板')
      })
      .catch(err => {
        console.error('复制失败:', err)
      })
  }
}

const clearModules = () => {
  if (confirm('确定要清空整个模块库吗？此操作不可恢复。')) {
    savedModules.value = [] // 清空内存中的模块
    localStorage.removeItem('savedModules') // 移除本地存储
    
    // 可选：显示清空成功消息
    showNotification('模块库已成功清空', 'success')
  }
}

// 显示通知的函数
const showNotification = (message, type = 'info') => {
  const notification = document.createElement('div')
  notification.className = `notification ${type}`
  notification.textContent = message
  
  document.body.appendChild(notification)
  
  // 添加动画效果
  setTimeout(() => {
    notification.classList.add('show')
  }, 10)
  
  // 3秒后移除
  setTimeout(() => {
    notification.classList.remove('show')
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}
</script>

<style scoped>
/* 全局样式 */
.design-page-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: auto;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  padding: 20px;
}

.module-design-container {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 30px;
  background: rgba(25, 35, 45, 0.85);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  min-height: calc(100vh - 40px);
  box-sizing: border-box;
}

.design-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.design-header h1 {
  font-size: 2.2rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 10px;
  background: linear-gradient(90deg, #1fa2ff, #46c195);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.design-header p {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.5;
}

/* 新布局 - 左右分栏 */
.design-layout {
  display: flex;
  gap: 25px;
}

.design-main {
  flex: 1;
  min-width: 0; /* 防止内容溢出 */
}

.module-library {
  width: 350px;
  min-width: 350px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 200px);
  overflow: hidden;
}

.library-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.library-header h2 {
  font-size: 1.5rem;
  color: #fff;
  margin: 0;
  font-weight: 600;
}

.module-count {
  background: rgba(31, 162, 255, 0.2);
  color: #1fa2ff;
  font-size: 0.85rem;
  padding: 5px 10px;
  border-radius: 12px;
}

.module-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 5px;
}

.empty-library {
  text-align: center;
  padding: 40px 20px;
  color: rgba(255, 255, 255, 0.6);
}

.empty-library svg {
  opacity: 0.5;
  margin-bottom: 15px;
}

.empty-library p {
  margin: 5px 0;
}

/* 模块项样式 */
.module-item {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 15px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.module-item:hover {
  background: rgba(31, 162, 255, 0.05);
  border-color: rgba(31, 162, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.module-info {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
}

.module-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: rgba(31, 162, 255, 0.15);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.module-content {
  flex: 1;
}

.module-content h3 {
  color: #fff;
  font-size: 1.1rem;
  margin: 0 0 8px 0;
}

.module-preview {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  line-height: 1.4;
}

.module-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid;
}

.action-button.view {
  background: transparent;
  color: #1fa2ff;
  border-color: rgba(31, 162, 255, 0.3);
}

.action-button.view:hover {
  background: rgba(31, 162, 255, 0.1);
}

.action-button.delete {
  background: transparent;
  color: #ff6b6b;
  border-color: rgba(255, 107, 107, 0.3);
}

.action-button.delete:hover {
  background: rgba(255, 107, 107, 0.1);
}

.action-button.download-fbt {
  background: transparent;
  color: #46c195; /* Green color for download */
  border-color: rgba(70, 193, 149, 0.3);
}

.action-button.download-fbt:hover {
  background: rgba(70, 193, 149, 0.1);
}

.module-time {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 10px;
  text-align: right;
}

/* 输入区域样式 */
.input-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  margin-bottom: 25px;
}

.input-container {
  margin-bottom: 15px;
}

.design-input {
  width: 100%;
  padding: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  resize: vertical;
  min-height: 150px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.design-input:focus {
  outline: none;
  border-color: #1fa2ff;
  box-shadow: 0 0 0 3px rgba(31, 162, 255, 0.2);
}

.design-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.submit-button {
  width: 100%;
  padding: 14px 20px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  background: linear-gradient(90deg, #1fa2ff, #46c195);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(31, 162, 255, 0.3);
}

.submit-button:disabled {
  background: rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.add-module-button {
  width: 100%;
  padding: 14px 20px;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-sizing: border-box;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.add-module-button:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

/* 结果区域样式 */
.result-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  padding: 20px;
  flex: 1;
}

.loading-dot {
  width: 10px;
  height: 10px;
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

.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ff6b6b;
  font-size: 1.1rem;
  padding: 20px;
  border-radius: 8px;
  background: rgba(255, 107, 107, 0.1);
  flex: 1;
}

.design-result {
  background: rgba(25, 35, 45, 0.9);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.result-header h2 {
  font-size: 1.5rem;
  color: #fff;
  margin: 0;
}

.result-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.copy-button {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.copy-button:hover {
  background: rgba(255, 255, 255, 0.15);
}

.result-content {
  background: rgba(15, 25, 35, 0.8);
  border-radius: 8px;
  padding: 15px;
  overflow: auto;
  flex: 1;
}

.result-content pre {
  margin: 0;
  color: #46c195;
  font-size: 1rem;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
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

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(31, 162, 255, 0.4);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(31, 162, 255, 0.6);
}

.clear-button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
  color: #ff6b6b;
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.clear-button:hover {
  background: rgba(255, 107, 107, 0.1);
}

.library-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.library-actions {
  display: flex;
  gap: 10px;
}

/* 新增通知样式 */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 8px;
  background: #2c3e50;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transform: translateY(-20px);
  opacity: 0;
  transition: all 0.3s ease;
  z-index: 1000;
  max-width: 300px;
  border-left: 4px solid #3498db;
}

.notification.show {
  transform: translateY(0);
  opacity: 1;
}

.notification.success {
  border-left-color: #2ecc71;
}

.notification.error {
  border-left-color: #e74c3c;
}

.system-button {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: rgba(31, 162, 255, 0.1);
  color: #1fa2ff;
  border: none;
}
</style>