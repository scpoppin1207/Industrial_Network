<template>
  <div class="app-container">
    <!-- 左侧画布区域 -->
    <div class="canvas-area">
      <VueFlow
        v-model:nodes="nodes"  
        v-model:edges="edges"
        :node-types="nodeTypes"              
        @pane-ready="onPaneReady"             
        @connect="onConnect"
        fit-view-on-init
        :nodes-draggable="true"
      >
        <template #node-A="props">
          <NodeA :v-bind="props" />
        </template>
      
        <template #node-B="props">
            <NodeB v-bind="props" />
        </template>

        <template #node-C="props">
            <NodeC v-bind="props" />
        </template>
      </VueFlow>
    </div>

    <!-- 右侧模块库 -->
    <div class="sidebar">
      <div class="sidebar-title">模块库</div>
      <div ref="nodeA" class="node" draggable>模块 A</div>
      <div ref="nodeB" class="node" draggable>模块 B</div>
      <div ref="nodeC" class="node" draggable>模块 C</div>
      <button @click="exportFlow">导出流程</button>
      <input type="file" id="importFile" accept=".json" @change="importFlow" />
    </div>
  </div>

  <ErrorOverlay :message="errorMessage" :errkey="errorKey" />
</template>

<script setup>
import { ref, onMounted, nextTick, markRaw } from 'vue'
import { VueFlow, addEdge, useVueFlow, MarkerType } from '@vue-flow/core'
import { validateConnection } from './utils/connectionRules' // 连接规则函数
import ErrorOverlay from './components/ErrorOverlay.vue' // 错误覆盖组件
import { ResizeRotateNode } from '@vue-flow/resize-rotate-node'

// 导入节点类型
import NodeA from './components/NodeA.vue'
import NodeB from './components/NodeB.vue'
import NodeC from './components/NodeC.vue'

// 注册节点类型， Vue Flow 会识别‘node-A’类型并在画布上渲染NodeA组件
const nodeTypes = {
  'node-A': markRaw(NodeA), // 使用 markRaw 确保组件不会被 Vue 的响应式系统处理
  'node-B': markRaw(NodeB),
  'node-C': markRaw(NodeC)
}

// 定义画布上的节点和边
const nodes = ref([]) // 画布上的节点数组
const edges = ref([]) // 画布上的边数组

// 用于引用side bar中的节点，而非实际的 Vue Flow 节点
const nodeA = ref(null)
const nodeB = ref(null)
const nodeC = ref(null)

// 错误处理相关
const errorMessage = ref('')
const errorKey = ref(0)

// 从 VueFlow 提供的 hook 中获取工具函数
const { project, addNodes, toObject } = useVueFlow() // 移除 setNodes 和 setEdges 的解构
const paneEl = ref(null) // pane DOM 元素
const vueFlowInstance = ref(null) // Vue Flow 实例

// 画布准备好后触发，用于绑定拖放事件
const onPaneReady = (instance) => {
  vueFlowInstance.value = instance // 存储 Vue Flow 实例
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
  e.preventDefault()
  const type = e.dataTransfer.getData('application/node-type') //A B C
  if (!type) return
  const canvasRect = paneEl.value.getBoundingClientRect()
  const viewportX = e.clientX - canvasRect.left
  const viewportY = e.clientY - canvasRect.top
  const position = project({ x: viewportX, y: viewportY })
  const nodeConfigs = {
    A: {
      type: 'node-A',
      data: { label: '模块 A' },
      handles: {
        inputs: [{ position: 'left', id: 'input-a' }],
        outputs: [{ position: 'right', id: 'output-a' }]
      }
    },
    B: {
      type: 'node-B',
      data: { label: '模块 B' },
      handles: {
        inputs: [{ position: 'left', id: 'input-b' }],
        outputs: [
          { position: 'left', id: 'output-b1' },
          { position: 'right', id: 'output-b2' },
          { position: 'bottom', id: 'output-b3' }
        ]
      }
    },
    C: {
      type: 'node-C',
      data: { label: '模块 C' },
      handles: {
        inputs: [{ position: 'top', id: 'input-c' }],
        outputs: []
      }
    }
  }
  const config = nodeConfigs[type]
  addNodes({
    id: `${type}-${Date.now()}`,
    type: config.type,
    position,
    data: {
      ...config.data,
      inputs: config.handles.inputs.map(h => h.id),
      outputs: config.handles.outputs.map(h => h.id),
      style: {
        background: '#fff',
        padding: '3px',
        borderRadius: '20px',
      },
    },
    draggable: true,
    connectable: true,
  })
}

// 连接事件处理
const onConnect = (params) => {
  const result = validateConnection(params, edges.value, nodes.value)
  if (!result.valid) {
    console.warn('❌ 连接无效:', result.reason)
    errorMessage.value = `连接错误：${result.code}`
    errorKey.value += 1
    return
  }
  edges.value = addEdge({
    ...params,
    animated: true,
    style: { stroke: '#674ea7', strokeWidth: 5 },
    markerEnd: { type: MarkerType.ArrowClosed, color: '#674ea7' },
  }, edges.value)
}

// 拖拽开始
const onDragStart = (event, type) => {
  console.log('🚀 dragstart:', type)
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('application/node-type', type)
  event.dataTransfer.setData('text/plain', `拖动模块 ${type}`)
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

// 导出功能
function exportFlow() {
  const flowData = toObject()
  const json = JSON.stringify(flowData, null, 2)
  const blob = new Blob([json], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'flow.json'
  a.click()
  URL.revokeObjectURL(url)
}

// 导入功能
function importFlow(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = function(e) {
      try {
        const content = e.target.result
        const data = JSON.parse(content)
        if (!vueFlowInstance.value) {
          console.error('❌ VueFlow 实例未初始化')
          errorMessage.value = '导入错误：画布未正确加载'
          errorKey.value += 1
          return
        }
        // 使用 VueFlow 实例的 setNodes 和 setEdges 清空并设置新数据
        vueFlowInstance.value.setNodes(data.nodes || [])
        vueFlowInstance.value.setEdges(data.edges || [])
        if (data.viewport) {
          vueFlowInstance.value.setViewport(data.viewport)
        }
      } catch (error) {
        console.error('❌ 导入失败: 无效的 JSON 文件', error)
        errorMessage.value = '导入错误：请确保选择有效的 JSON 文件'
        errorKey.value += 1
      }
    }
    reader.readAsText(file)
  }
}
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
  user-select: none;        
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