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
        @nodes-change = "onNodesChange"
        @edges-change = "onEdgesChange"
      >
       <MiniMap pannable zoomable />
      <!-- Vue flow的node-types属性绑定在nodeTypes变量上 Vue flow的pane-ready事件绑定在onPaneReady函数上，事件发生会触发onPaneReady函数 -->

       <template #node-A="props">
          <NodeA v-bind="props" />
       </template>
      
        <template #node-B="props">
            <NodeB v-bind="props" />
        </template>

        <template #node-C="props">
            <NodeC v-bind="props" />
        </template>

        <template #node-D="props">
            <NodeD v-bind="props" />
        </template>

      </VueFlow>
    </div>

    <!-- 右侧模块库 -->
    <div class="sidebar">
      <div class="sidebar-title">模块库</div>
      <div ref="nodeA" class="node" draggable>输送机</div>
      <div ref="nodeB" class="node" draggable>移载机</div>
      <div ref="nodeC" class="node" draggable>提升机</div>
      <div ref="nodeD" class="node" draggable>货架</div>
      <!-- <button @click="handleExport">导出流程</button> -->
      <!-- 可选导出形式 -->
      <button @click="handleExport('json')">导出 JSON</button>
      <button @click="handleExport('sys')">导出 SYS</button>
      <!-- <input type="file" id="importFile" accept=".json" @change="handleImport" /> -->
      <!-- 导入按钮，只负责触发 file input -->
      <input type="file" accept=".json" @change="handleImport" ref="fileInputRef" style="display: none;" />
      <button @click="fileInputRef.click()">导入 JSON</button>
    </div>

  <WelcomeDialog v-model="dialogVisible" @flow-generated="handleFlowGenerated" />
  <ErrorOverlay :message="errorMessage" :errkey="errorKey" />
  </div>
 
</template>

<script setup>
import { ref, onMounted , nextTick, markRaw} from 'vue'
import { VueFlow, addEdge, useVueFlow, MarkerType, applyNodeChanges, applyEdgeChanges } from '@vue-flow/core'
import { MiniMap } from '@vue-flow/minimap'
import '@vue-flow/minimap/dist/style.css'
import { validateConnection } from './utils/connectionRules' // 连接规则函数
import { exportFlow, importFlow } from './utils/importExport'
import ErrorOverlay from './components/ErrorOverlay.vue' // 错误覆盖组件
import WelcomeDialog from './components/Dialog.vue'
const dialogVisible = ref(true)

// 导入节点类型
import NodeA from './components/NodeA.vue'
import NodeB from './components/NodeB.vue'
import NodeC from './components/NodeC.vue'
import NodeD from './components/NodeD.vue'

// 注册节点类型， Vue Flow 会识别‘node-A’类型并在画布上渲染NodeA组件
const nodeTypes = {
  'node-A': markRaw(NodeA), // 使用 markRaw 确保组件不会被 Vue 的响应式系统处理
  'node-B': markRaw(NodeB),
  'node-C': markRaw(NodeC),
  'node-D': markRaw(NodeD), 
}

// 定义画布上的节点和边
// 使用 ref 管理节点和边
const nodes = ref([])
const edges = ref([])
const { project, addNodes, addEdges, fitView } = useVueFlow()
const vueFlowInstance = ref(null)
const fileInputRef = ref(null)
const paneEl = ref(null)
let pendingFlow = null


// 用于引用side bar中的节点，而非实际的 Vue Flow 节点
const nodeA = ref(null)
const nodeB = ref(null)
const nodeC = ref(null)
const nodeD = ref(null) 

// 错误处理相关
const errorMessage = ref('')
const errorKey = ref(0)



// 画布准备好后触发，用于绑定拖放事件
const onPaneReady = (instance) => {
  vueFlowInstance.value = instance

  // 通过 DOM 查询直接获取 pane 元素
  const pane = document.querySelector('.vue-flow__pane')
  if (!pane) {
    console.error('❌ 无法获取 .vue-flow__pane 元素，请检查是否正确挂载 VueFlow')
    return
  }
  paneEl.value = pane
  // pane元素添加拖放事件监听器，'dragover'事件触发时调用匿名函数
  pane.addEventListener('dragover', (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
  }) 
  // pane元素添加拖放事件监听器，'drop'事件触发时调用handleDrop函数
  pane.addEventListener('drop', handleDrop) 
  console.log('☺️pane start')

  if (pendingFlow) {
    // 如果有待处理的 flow，直接设置到 pane
    handleFlowGenerated(pendingFlow)
    pendingFlow = null // 清空待处理 flow
  }
}

// 拖放添加节点处理函数
const handleDrop = (e) => {
  // e 表示拖放事件
  e.preventDefault()

  // 获取拖放的节点类型
  const type = e.dataTransfer.getData('application/node-type') //A B C
  if (!type) return

  // 获取鼠标在canvas中的位置
  const canvasRect = paneEl.value.getBoundingClientRect() // 获取画布的边界矩形
  const viewportX = e.clientX - canvasRect.left
  const viewportY = e.clientY - canvasRect.top

  // 转换为 Vue Flow 坐标 （逻辑坐标）
  // project 是 Vue Flow 提供的函数，用于将屏幕坐标转换为逻辑坐标
  const position = project({ x: viewportX, y: viewportY })

  // 根据拖放的节点类型，获取对应的节点配置
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
          { position: 'top', id: 'output-b1' },
          { position: 'bottom', id: 'output-b2' },
          { position: 'right', id: 'output-b3' }
        ]
      }
    },
    C: {
      type: 'node-C',
      data: { label: '模块 C' },
      handles: {
        inputs: [{ position: 'top', id: 'input-c' }],
        outputs: [{ position: 'right', id: 'output-c' }]
      }
    },
    D: {
      type: 'node-D',
      data: { label: '模块 D' },
      handles: {
        inputs: [{ position: 'left', id: 'input-d' }],
        outputs: [{ position: 'right', id: 'output-d'}],
      }
    }
  }
  
  const config = nodeConfigs[type]
  console.log('创建节点时的 config.data:', config.data) 
  // 添加节点
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
        padding: '5px',
        borderRadius: '20px',
    },
    },
    draggable: true,
    connectable: true,
  })
  //map 是 JavaScript 数组的一个方法，用来遍历数组并返回一个新数组 (h=> h.id) 是一个箭头函数，表示将每个 handle 的 id 提取出来
}

// 连接事件处理
// 当用户在 Vue Flow 画布上连接两个节点时，Vue Flow 会触发 connect 事件，onConnect 函数就会被调用，
// 参数是连接的信息（如起点、终点等）。
const onConnect = (params) => {
  const result = validateConnection(params, edges.value, nodes.value)
  if (!result.valid) {
    console.warn('❌ 连接无效:', result.reason)
    errorMessage.value = `连接错误：${result.code}`
    errorKey.value += 1
    return
  }
  // 加入楼层处理逻辑
  const sourceNode = nodes.value.find(n => n.id === params.source)
  const targetNode = nodes.value.find(n => n.id === params.target)
  if (sourceNode && targetNode) {
  // 判断是否是提升机（举例：假设 type 为 'node-C' 的是提升机）
  const isSourceElevator = sourceNode.type === 'node-C'
  const isTargetElevator = targetNode.type === 'node-C'

  // 获取 source 楼层
  const sourceFloor = sourceNode.data.floor ?? 1

  if (isSourceElevator && !isTargetElevator) {
    targetNode.data.floor = sourceFloor + 1
  } else if (!isSourceElevator && isTargetElevator) {
    targetNode.data.floor = sourceFloor
  } else if (!isSourceElevator && !isTargetElevator) {
    targetNode.data.floor = sourceFloor
  }

  // 触发响应式更新（Vue 不检测深层变更）
  targetNode.data = { ...targetNode.data }
  }

  // 修改边处理函数
  addEdges({
    ...params,
    animated: true,       // 边是否动画
    style: {                 // 可选：边的线条样式
      stroke: '#674ea7',
      strokeWidth: 5,
    },
    markerEnd: {             // 可选：终点箭头样式
      type: MarkerType.ArrowClosed,
      color: '#674ea7',
    },        // 可选：边的类型，default / step / smoothstep / straight 等
  })
}


// 拖拽开始
const onDragStart = (event, type) => {
  // 设置拖拽开始时，拖拽事件中的节点类型，键名为 'application/node-type'，值为节点类型
  console.log('🚀 dragstart:', type)
  event.dataTransfer.effectAllowed = 'move' // 明确设置拖动效果
  event.dataTransfer.setData('application/node-type', type)  //A B C
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
  if (nodeD.value) {
    nodeD.value.addEventListener('dragstart', (e) => onDragStart(e, 'D'))
    nodeD.value.addEventListener('dragend', onDragEnd)
  }
})

// 导出和导入处理
// const handleExport = () => {
//   exportFlow(vueFlowInstance.value, (message) => {
//     errorMessage.value = message
//     errorKey.value += 1
//   })
// }

// 新的导出函数
const handleExport = (format = 'json') => {
  exportFlow(vueFlowInstance.value, (message) => {
    errorMessage.value = message
    errorKey.value += 1
  }, format === 'sys')
}

function onNodesChange(changes) {
  nodes.value = applyNodeChanges(changes, nodes.value)
}

function onEdgesChange(changes) {
  edges.value = applyEdgeChanges(changes, edges.value)
}


/** ———— 导入按钮绑定 —— **/
function handleImport(event) {
  /**
   * 原来我们写的是：importFlow(vueFlowInstance.value, event, onError)
   * 现在改为：importFlow(event, onSuccess, onError)
   */
  importFlow(
    event,
    (data) => {
      nodes.value = data.nodes || []
      edges.value = data.edges || []

      // 2. 如果有 viewport，则设置
      if (data.viewport) {
        vueFlowInstance.value.setViewport(data.viewport)
      }

      // 3. 最后 fitView
      if (vueFlowInstance.value) {
        fitView()
      }
    },
    (msg) => {
      errorMessage.value = msg
      errorKey.value += 1
    }
  )
}

/** ———— “AI 生成流程” 的回调 —— **/
function handleFlowGenerated(flow) {
  if (vueFlowInstance.value) {
    try {
      nodes.value = flow.nodes || []
      edges.value = flow.edges || []

      // 如果有 viewport 信息，就让实例设置一下
      if (flow.viewport) {
        vueFlowInstance.value.setViewport(flow.viewport)
      }

      // 导入完成或生成完成后，把画布 fit 到可视区
      fitView()
    } catch (error) {
      console.error('❌ 处理流程生成时出错:', error)
      errorMessage.value = '流程生成失败，请检查数据格式'
      errorKey.value += 1
    }
  } else {
    // 还没 ready，把 flow 缓存起来，等 pane-ready 再真正设置
    pendingFlow = flow
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
  background-image: linear-gradient(to right, #ccc 1px, transparent 1px),
                    linear-gradient(to bottom, #ccc 1px, transparent 1px);
  background-size: 20px 20px; /* 每个网格20px */
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