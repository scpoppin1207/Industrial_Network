<template>
    <div class="app-container">
      <!-- 左侧画布区域 -->
      <div class="canvas-area" @keydown.delete="handleKeyDelete" tabindex="0">
        <div class="background-animation"></div>
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
          @node-click = "onNodeClick"
        >
        <MiniMap pannable zoomable :node-color="nodeColor" />


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

          <template v-for="(nodeConfig, index) in customNodes" :key="`custom-node-${index}`" #[`node-custom-${nodeConfig.id}`]="props">
              <CustomNode v-bind="props" :nodeConfig="nodeConfig" />
          </template>

        </VueFlow>
      </div>

      <!-- 右侧模块库 -->
      <div class="sidebar">
        <div class="sidebar-title">模块库</div>
        <div ref="nodeA" class="node" draggable>
          <div class="node-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 4H8c-1.4 0-2.5 1.1-2.5 2.5v11c0 1.4 1.1 2.5 2.5 2.5h8c1.4 0 2.5-1.1 2.5-2.5v-11c0-1.4-1.1-2.5-2.5-2.5Z"/>
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18 6.5c0-1.4-1.1-2.5-2.5-2.5h-7c-1.4 0-2.5 1.1-2.5 2.5v11c0 1.4 1.1 2.5 2.5 2.5h7c1.4 0 2.5-1.1 2.5-2.5v-11Z"/>
            </svg>
          </div>
          <span>输送机</span>
        </div>
        <div ref="nodeB" class="node" draggable>
          <div class="node-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 6h6M9 12h6M9 18h6"/>
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.8 21.5h14.4c1.3 0 2.3-1 2.3-2.3V4.8c0-1.3-1-2.3-2.3-2.3H4.8C3.5 2.5 2.5 3.5 2.5 4.8v14.4c0 1.3 1 2.3 2.3 2.3Z"/>
            </svg>
          </div>
          <span>移载机</span>
        </div>
        <div ref="nodeC" class="node" draggable>
          <div class="node-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 5v14m0 0-3-3m3 3 3-3"/>
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.8 21.5h14.4c1.3 0 2.3-1 2.3-2.3V4.8c0-1.3-1-2.3-2.3-2.3H4.8C3.5 2.5 2.5 3.5 2.5 4.8v14.4c0 1.3 1 2.3 2.3 2.3Z"/>
            </svg>
          </div>
          <span>提升机</span>
        </div>
        <div ref="nodeD" class="node" draggable>
          <div class="node-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 9v12m0 0h14M5 21V9m14 0v12M5 9h14M5 9V3m14 6V3"/>
            </svg>
          </div>
          <span>货架</span>
        </div>

        <div 
        v-for="(node, index) in customNodes" 
        :key="index" 
        class="node custom-node" 
        draggable
        @dragstart="e => onCustomDragStart(e, node)"
        @dragend="onDragEnd"
      >
          <div class="node-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 4H8c-1.4 0-2.5 1.1-2.5 2.5v11c0 1.4 1.1 2.5 2.5 2.5h8c1.4 0 2.5-1.1 2.5-2.5v-11c0-1.4-1.1-2.5-2.5-2.5Z"/>
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18 6.5c0-1.4-1.1-2.5-2.5-2.5h-7c-1.4 0-2.5 1.1-2.5 2.5v11c0 1.4 1.1 2.5 2.5 2.5h7c1.4 0 2.5-1.1 2.5-2.5v-11Z"/>
            </svg>
          </div>
          <span>{{ node.name }}</span>
        </div>


        <div class="export-buttons">
          <button class="export-btn" @click="handleExport('json')">导出 JSON</button>
          <button class="export-btn" @click="handleExport('sys')">导出 SYS</button>
          <input type="file" accept=".json" @change="handleImport" ref="fileInputRef" style="display: none;" />
          <button class="export-btn" @click="fileInputRef.click()">导入 JSON</button>
          <button class="export-btn" @click="goToBlock">前往模块设计</button>
        </div>

      </div>

    <WelcomeDialog v-model="dialogVisible" @flow-generated="handleFlowGenerated" />
    <ErrorOverlay :message="errorMessage" :errkey="errorKey" />
    </div>
</template>

<script setup>
import EntrySelector from './EntrySelector.vue'
const entry = ref('') // '' 表示未选择，'custom' 或 'system'
import { watch,ref, onMounted , nextTick, markRaw} from 'vue'
import { VueFlow, addEdge, useVueFlow, MarkerType, applyNodeChanges, applyEdgeChanges } from '@vue-flow/core'
import { MiniMap } from '@vue-flow/minimap'
import { useRouter } from 'vue-router'
import '@vue-flow/minimap/dist/style.css'
import { validateConnection } from '../utils/connectionRules' // 连接规则函数
import { exportFlow, importFlow } from '../utils/importExport'
import ErrorOverlay from './ErrorOverlay.vue' // 错误覆盖组件
import WelcomeDialog from './Dialog.vue'
const dialogVisible = ref(true)

const router = useRouter()

const goToBlock = () => {
  router.push('../block')
}

// 导入节点类型
import NodeA from './NodeA.vue'
import NodeB from './NodeB.vue'
import NodeC from './NodeC.vue'
import NodeD from './NodeD.vue'

// 导入自定义节点组件
import CustomNode from './CustomNode.vue'

// 注册节点类型， Vue Flow 会识别‘node-A’类型并在画布上渲染NodeA组件
const nodeTypes = {
  'node-A': markRaw(NodeA), // 使用 markRaw 确保组件不会被 Vue 的响应式系统处理
  'node-B': markRaw(NodeB),
  'node-C': markRaw(NodeC),
  'node-D': markRaw(NodeD), 
}

// 定义画布上的节点和边
const nodes = ref([])
const edges = ref([])
const { project, addNodes, addEdges, fitView, findNode } = useVueFlow()
const vueFlowInstance = ref(null)
const fileInputRef = ref(null)
const paneEl = ref(null)
const selectedNodeId = ref(null) // 存储当前选中的节点ID
let pendingFlow = null

// 错误处理相关
const errorMessage = ref('')
const errorKey = ref(0)

// 用于引用side bar中的节点，而非实际的 Vue Flow 节点
const nodeA = ref(null)
const nodeB = ref(null)
const nodeC = ref(null)
const nodeD = ref(null) 

// 自定义节点配置
const customNodes = ref([])

// 从localStorage加载自定义模块
const loadCustomModules = () => {
  try {
    const saved = localStorage.getItem('savedModules')
    if (!saved) return []
    
    const modules = JSON.parse(saved)
    return modules.map(module => {
      // 解析输入输出数量
      const inputCount = module.content.inputs?.length || 0
      const outputCount = module.content.outputs?.length || 0
      console.log('加载自定义模块:', module.name, '输入:', inputCount, '输出:', outputCount)
      return {
        id: module.id,
        name: module.name,
        content: module.content,
        inputs: inputCount,
        outputs: outputCount,
        timestamp: module.timestamp,
        userInput: module.userInput,
        type: `custom-${module.id}` // 唯一的节点类型标识
      }
    })
  } catch (e) {
    console.error('解析自定义模块失败:', e)
    return []
  }
}

const registerCustomNodeTypes = () => {
  customNodes.value.forEach(node => {
    if (!nodeTypes[node.name]) {
      nodeTypes[node.name] = markRaw(CustomNode)
      console.log(`成功注册自定义节点类型: ${node.name}`)
    }
  })
}

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

// 节点点击事件
const onNodeClick = (event) => {
  const node = event.node; // Extract the node object from the event
  if (node && node.id) {
    console.log('Node ID:', node.id); // Log the node ID
    selectedNodeId.value = node.id; // Update the selectedNodeId
  } else {
    console.warn('Node data is not available or node ID is missing');
  }
};

// 修改后的 handleKeyDelete 函数
const handleKeyDelete = (event) => {
  // 调试信息
  console.log('Delete key pressed:', document.activeElement);
  console.log('Delete键按下', {
    selectedNodeId: selectedNodeId.value,
    vueFlowInstance: !!vueFlowInstance.value,
    event
  })

  if (!selectedNodeId.value) {
    console.warn('没有选中的节点')
    return
  }

  // 阻止默认行为（如果有）
  event.preventDefault()

  // 确保VueFlow实例可用
  if (!vueFlowInstance.value) {
    console.error('VueFlow实例未初始化')
    return
  }

  // 1. 找出所有要删除的边
  const edgeIdsToRemove = edges.value
    .filter(edge => edge.source === selectedNodeId.value || 
                   edge.target === selectedNodeId.value)
    .map(edge => edge.id)

  // 调试信息
  console.log('要删除的边:', edgeIdsToRemove)

  // 2. 获取要删除的节点
  const nodeToRemove = findNode(selectedNodeId.value)
  console.log('要删除的节点:', nodeToRemove)

  try {
    // 3. 执行删除
    if (edgeIdsToRemove.length > 0) {
      vueFlowInstance.value.removeEdges(edgeIdsToRemove)
    }
    vueFlowInstance.value.removeNodes([selectedNodeId.value])

    // 4. 特殊处理提升机删除
    if (nodeToRemove?.type === 'node-C') {
      handleElevatorRemoval(nodeToRemove)
    }

    selectedNodeId.value = null
    fitView()
    console.log('删除成功')
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 处理提升机删除后的楼层逻辑
const handleElevatorRemoval = (removedElevator) => {
  const elevatorFloor = removedElevator.data.floor || 1
  
  // 找出所有连接到该提升机的节点
  const connectedNodes = edges.value.reduce((acc, edge) => {
    if (edge.source === removedElevator.id) {
      const node = findNode(edge.target)
      if (node) acc.push(node)
    }
    if (edge.target === removedElevator.id) {
      const node = findNode(edge.source)
      if (node) acc.push(node)
    }
    return acc
  }, [])
  
  // 更新这些节点的楼层
  connectedNodes.forEach(node => {
    if (node.type !== 'node-C') { // 不是提升机
      node.data.floor = elevatorFloor
    }
  })
}

// 拖放添加节点处理函数
const handleDrop = (e) => {
  e.preventDefault()

  // 优先获取自定义节点配置
  const nodeConfigJson = e.dataTransfer.getData('application/node-config')
  if (nodeConfigJson) {
    console.log('拖放自定义节点配置:', nodeConfigJson)
    let nodeConfig = null
    try {
      nodeConfig = JSON.parse(nodeConfigJson)
    } catch (e) {
      console.error('解析自定义节点配置失败:', e)
      return
    }
    // 获取鼠标在canvas中的位置
    const canvasRect = paneEl.value.getBoundingClientRect()
    const viewportX = e.clientX - canvasRect.left
    const viewportY = e.clientY - canvasRect.top
    const position = project({ x: viewportX, y: viewportY })
    addCustomNode(nodeConfig, position)
    return
  }

  // 基础节点拖拽
  const type = e.dataTransfer.getData('application/node-type')

  // ...原有基础节点逻辑...
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
  if (!config) {
    console.warn('未知的基础节点类型:', type)
    return
  }

  const canvasRect = paneEl.value.getBoundingClientRect()
  const viewportX = e.clientX - canvasRect.left
  const viewportY = e.clientY - canvasRect.top
  const position = project({ x: viewportX, y: viewportY })

  addNodes({
    id: `${type}-${Date.now()}`,
    type: config.type,
    position,
    data: {
      ...config.data,
      inputs: config.handles.inputs.map(h => h.id),
      outputs: config.handles.outputs.map(h => h.id),
      floor: 1, // 默认楼层
      style: {
        background: '#fff',
        padding: '5px',
        borderRadius: '20px',
      },
    },
    draggable: true,
    connectable: true,
  })
}

// 连接处理函数
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
      stroke: '#1fa2ff',
      strokeWidth: 2,
    },
    markerEnd: {             // 可选：终点箭头样式
      type: MarkerType.ArrowClosed,
      color: '#1fa2ff',
    },        // 可选：边的类型，default / step / smoothstep / straight 等
  })
}


// 自定义节点拖拽开始
const onCustomDragStart = (event, nodeConfig) => {
  console.log('🚀 自定义节点拖拽开始:', nodeConfig.name)
  event.dataTransfer.effectAllowed = 'move'
  // 存储完整的节点配置
  event.dataTransfer.setData('application/node-type', nodeConfig.type)
  event.dataTransfer.setData('application/node-config', JSON.stringify(nodeConfig))
  event.dataTransfer.setData('text/plain', `拖动自定义模块: ${nodeConfig.name}`)
  event.target.style.opacity = '0.5'
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
  // 加载自定义模块
  customNodes.value = loadCustomModules()
  registerCustomNodeTypes()
})


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

// MiniMap 节点颜色函数
const nodeColor = (node) => {
  switch (node.type) {
    case 'node-A': return '#1fa2ff';
    case 'node-B': return '#8643ff';
    case 'node-C': return '#a6ffcb';
    case 'node-D': return '#ff9a8b';
    default: return '#ffcc00';
  }
};

// 添加自定义节点到画布
const addCustomNode = (nodeConfig, position) => {
  const inputCount = nodeConfig.inputs
  const outputCount = nodeConfig.outputs
  
  // 创建输入输出连接点
  const inputs = Array.from({ length: inputCount }, (_, i) => ({
    position: 'left',
    id: `input-${i}`
  }))
  
  const outputs = Array.from({ length: outputCount }, (_, i) => ({
    position: 'right',
    id: `output-${i}`
  }))

  console.log(`添加自定义节点id: ${nodeConfig.type}-${Date.now()}`)
  console.log(`添加自定义节点type: ${nodeConfig.type}`)



  // 添加节点
  addNodes({
    id: `${nodeConfig.type}-${Date.now()}`,
    type: nodeConfig.type, // 使用自定义节点类型
    position,
    data: {
      label: nodeConfig.name,
      inputs: inputs.map(h => h.id),
      outputs: outputs.map(h => h.id),
      nodeConfig: nodeConfig, // 传递完整配置
      floor: 1, // 默认楼层
      style: {
        background: '#fff',
        padding: '5px',
        borderRadius: '20px',
      },
    },
    draggable: true,
    connectable: true,
  })
  
  console.log(`✅ 添加自定义节点: ${nodeConfig.name}`)
}

</script>

<style>
/* 确保前端铺满屏幕 */
html, body, #app {
  height: 100%;
  margin: 0;
}
/* 添加深色渐变背景 */
.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
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

.canvas-area {
  flex: 1;
  position: relative;
  background-color: rgba(0, 0, 0, 0.2);
  background-image: 
    linear-gradient(to right, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  z-index: 1;
  border-radius: 0;
  overflow: hidden;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
}

.custom-node {
  background-color: rgba(31, 162, 255, 0.1);
  border: 1px solid rgba(31, 162, 255, 0.5);
}

.custom-node .node-icon svg {
  color: #1fa2ff;
}

.custom-node:hover {
  background-color: rgba(31, 162, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(31, 162, 255, 0.2);
}



.sidebar {
  user-select: none;        
  width: 360px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.12);
  padding: 25px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: 20px;
  /* 优化布局 */
  overflow-y: auto;
  max-height: 100vh;
}

.sidebar-title {
  font-size: 1.6rem;
  font-weight: 600;
  color: white;
  margin-bottom: 15px;
  text-align: center;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  position: relative;
  padding-bottom: 15px;
}

.sidebar-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, #1fa2ff, #a6ffcb);
  border-radius: 2px;
}

.node {
  padding: 18px 25px;
  margin-bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 15px;
  cursor: grab;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 15px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.node-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(31, 162, 255, 0.2), rgba(166, 255, 203, 0.2));
}

.node-icon svg {
  width: 24px;
  height: 24px;
  stroke: #1fa2ff;
}

.node:nth-child(3) .node-icon {
  background: linear-gradient(135deg, rgba(134, 67, 255, 0.2), rgba(151, 60, 255, 0.2));
}

.node:nth-child(3) .node-icon svg {
  stroke: #8643ff;
}

.node:nth-child(4) .node-icon {
  background: linear-gradient(135deg, rgba(166, 255, 203, 0.2), rgba(86, 204, 242, 0.2));
}

.node:nth-child(4) .node-icon svg {
  stroke: #a6ffcb;
}

.node:nth-child(5) .node-icon {
  background: linear-gradient(135deg, rgba(255, 154, 139, 0.2), rgba(255, 107, 107, 0.2));
}

.node:nth-child(5) .node-icon svg {
  stroke: #ff9a8b;
}

.node:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.node:active {
  cursor: grabbing;
  transform: scale(0.98) translateY(0);
}

.node {
  -webkit-user-drag: element; /* macOS Safari 支持 + 拖放的关键 */
}

.export-buttons {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.export-btn {
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.export-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
}

.vue-flow__node {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.vue-flow__node.selected {
  box-shadow: 0 0 0 2px #1fa2ff;
}

.vue-flow__edge-path {
  stroke: #1fa2ff;
  stroke-width: 2;
}

.vue-flow__minimap {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.vue-flow__minimap-mask {
  fill: rgba(255, 255, 255, 0.1);
}

.vue-flow__minimap-node {
  stroke: none;
}

@media (max-width: 1200px) {
  .sidebar {
    width: 300px;
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    padding: 15px;
    border-left: none;
    border-top: 1px solid rgba(255, 255, 255, 0.12);
  }

  .export-buttons {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .export-btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>