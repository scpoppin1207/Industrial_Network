<template>
  <div class="app-container">
    <!-- 左侧画布区域 -->
    <div class="canvas-area">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        @pane-ready="onPaneReady"
        @connect="onConnect"
        fit-view-on-init
        :nodes-draggable="true"
      >
      </VueFlow>
    </div>

    <!-- 右侧模块库 -->
    <div class="sidebar">
      <div class="sidebar-title">模块库</div>
      <div ref="nodeA" class="node" draggable>模块 A</div>
      <div ref="nodeB" class="node" draggable>模块 B</div>
      <div ref="nodeC" class="node" draggable>模块 C</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted , nextTick} from 'vue'
import { VueFlow, addEdge, useVueFlow } from '@vue-flow/core'

// 需要先定义并导出这些 ref
const nodeA = ref(null)
const nodeB = ref(null)
const nodeC = ref(null)


// 从 VueFlow 提供的 hook 中获取工具函数
const { project, addNodes } = useVueFlow()
const paneEl = ref(null) // pane DOM 元素

// 画布准备好后触发，用于绑定拖放事件
const onPaneReady = () => {
  // 通过 DOM 查询直接获取 pane 元素
  const pane = document.querySelector('.vue-flow__pane')
  if (!pane) {
    console.error('❌ 无法获取 .vue-flow__pane 元素，请检查是否正确挂载 VueFlow')
    return
  }
  paneEl.value = pane

  pane.addEventListener('dragover', (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
  })  
  pane.addEventListener('drop', handleDrop)
  console.log('☺️pane start')
}

// 拖放添加节点处理函数
const handleDrop = (e) => {
  // e 表示拖放事件
  e.preventDefault()

  // 获取拖放的节点类型
  const type = e.dataTransfer.getData('application/node-type')
  if (!type) return

  // 获取鼠标在canvas中的位置
  const canvasRect = paneEl.value.getBoundingClientRect() // 获取画布的边界矩形
  const viewportX = e.clientX - canvasRect.left
  const viewportY = e.clientY - canvasRect.top

  // 转换为 Vue Flow 坐标 （逻辑坐标）
  // project 是 Vue Flow 提供的函数，用于将屏幕坐标转换为逻辑坐标
  const position = project({ x: viewportX, y: viewportY })

  // 添加节点
  addNodes({
    id: `${type}-${Date.now()}`,
    type: 'default',
    position,
    data: { label: `模块 ${type}` },
    draggable: true
  })
}


// 连接事件处理
// 当用户在 Vue Flow 画布上连接两个节点时，Vue Flow 会触发 connect 事件，onConnect 函数就会被调用，
// 参数是连接的信息（如起点、终点等）。
const onConnect = (params) => {
  edges.value = addEdge({ ...params, animated: true }, edges.value)
}

//edges.value是当前的边 数组
//params：Vue Flow 触发 connect 事件时传递的参数，包含新连线的起点、终点等信息
//onConnect 函数会将新连接的边添加到 edges 数组中，并设置为动画状态。

// 拖拽开始
const onDragStart = (event, type) => {
  // 设置拖拽开始时，拖拽事件中的节点类型，键名为 'application/node-type'，值为节点类型
  console.log('🚀 dragstart:', type)
  event.dataTransfer.effectAllowed = 'move' // 明确设置拖动效果
  event.dataTransfer.setData('application/node-type', type)
  event.dataTransfer.setData('text/plain', `拖动模块 ${type}`)
  // 设置拖拽时的样式
  event.target.style.opacity = '0.5'
}

// 拖拽结束恢复样式
const onDragEnd = (event) => {
  event.target.style.opacity = '1'
}

onMounted(async () => {
  await nextTick()
  if (nodeA.value) {
    nodeA.value.addEventListener('dragstart', (e) => onDragStart(e, 'A'))
    nodeA.value.addEventListener('dragend', onDragEnd)
  }
  if (nodeB.value) {
    nodeB.value.addEventListener('dragstart', (e) => onDragStart(e, 'B'))
    nodeB.value.addEventListener('dragend', onDragEnd)
  }
  if (nodeC.value) {
    nodeC.value.addEventListener('dragstart', (e) => onDragStart(e, 'C'))
    nodeC.value.addEventListener('dragend', onDragEnd)
  }
})

</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.canvas-area {
  flex: 1;
  position: relative;
  background-color: #f0f0f0;
}

.sidebar {
  width: 360px;
  background: white;
  border-left: 1px solid #eee;
  padding: 16px;
}

.sidebar-title {
  font-weight: bold;
  margin-bottom: 12px;
}

.node {
  padding: 12px;
  margin-bottom: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: grab;
  transition: transform 0.1s;
}

.node:active {
  cursor: grabbing;
  transform: scale(0.98);
}

.node {
  -webkit-user-drag: element; /* macOS Safari 支持 */
}
</style>