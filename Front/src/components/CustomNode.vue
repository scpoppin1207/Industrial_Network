<template>
  <div class="custom-node" :style="style">
    <!-- 节点标题区域 -->
    <div class="node-header">
      <div class="node-type-badge">自定义</div>
      <div class="node-title">{{ data.label }}</div>
    </div>
    
    <!-- 输入点 -->
    <div class="inputs">
      <Handle 
        v-for="(input, index) in inputs" 
        :key="input.id"
        :id="input.id"
        type="target"
        :position="Position.Left"
        :style="{ top: inputPosition(index, inputs.length) }"
        :class="['custom-handle', 'input-handle']"
      />
    </div>
    
    <!-- 输出点 -->
    <div class="outputs">
      <Handle 
        v-for="(output, index) in outputs" 
        :key="output.id"
        :id="output.id"
        type="source"
        :position="Position.Right"
        :style="{ top: outputPosition(index, outputs.length) }"
        :class="['custom-handle', 'output-handle']"
      />
    </div>
    
    <!-- 模块信息区域 -->
    <div class="info-section">
      <div class="module-description">
        <div v-if="nodeConfig.des" class="description-content">
          {{ nodeConfig.des }}
        </div>
        <div v-else class="no-description">
          自定义模块
        </div>
      </div>
      <div class="connector-info">
        <span>{{ inputs.length }} 输入</span>
        <span>{{ outputs.length }} 输出</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Handle, Position } from '@vue-flow/core'
import { computed } from 'vue'

const props = defineProps({
  id: String,
  type: String,
  selected: Boolean,
  data: Object,
  nodeConfig: Object
})

// 计算输入输出点的位置
const inputPosition = (index, total) => {
  return `${(index + 1) * 100 / (total + 1)}%`;
}

const outputPosition = (index, total) => {
  return `${(index + 1) * 100 / (total + 1)}%`;
}

// 设置节点样式
const style = computed(() => ({
  backgroundColor: getFloorColor(1),
  border: `2px solid ${props.selected ? '#1890ff' : '#8643ff'}`,
  boxShadow: props.selected ? '0 0 8px rgba(24, 144, 255, 0.5)' : '0 2px 6px rgba(0, 0, 0, 0.1)',
}))

// 楼层颜色计算
const getFloorColor = () => {
  // 固定浅灰色背景，不需要动态楼层
  return '#f8f9fa'
}

// 提取节点配置
const nodeConfig = computed(() => props.data.nodeConfig || {})

// 设置输入输出点
const inputs = computed(() => {
  const count = props.nodeConfig?.inputs || 0
  return Array.from({ length: count }, (_, i) => ({
    id: `input-${i}`,
    position: Position.Left
  }))
})

const outputs = computed(() => {
  const count = props.nodeConfig?.outputs || 0
  return Array.from({ length: count }, (_, i) => ({
    id: `output-${i}`,
    position: Position.Right
  }))
})
</script>

<style scoped>
.custom-node {
  position: relative;
  font-family: 'Arial', sans-serif;
  font-size: 12px;
  display: flex;
  flex-direction: column;
  width: 160px;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

/* 节点顶部标题栏 */
.node-header {
  display: flex;
  align-items: center;
  padding: 6px 8px;
  background: linear-gradient(135deg, #8643ff, #6a11cb);
  height: 30px;
}

.node-type-badge {
  background-color: #1fa2ff;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 6px;
  white-space: nowrap;
}

.node-title {
  color: white;
  font-weight: bold;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
}

/* 信息区域 */
.info-section {
  display: flex;
  flex-direction: column;
  height: calc(100% - 30px);
  padding: 10px;
  background-color: #f8f9fa;
}

.module-description {
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 11px;
  color: #555;
  line-height: 1.4;
  text-align: center;
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  max-height: 70px;
}

.description-content {
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 限制3行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-description {
  font-style: italic;
  color: #aaa;
}

/* 连接点信息 */
.connector-info {
  display: flex;
  justify-content: space-between;
  padding: 4px 8px 0;
  font-size: 10px;
  color: #666;
  margin-top: auto;
}

/* 连接点样式 */
.custom-handle {
  width: 16px;
  height: 16px;
  background: white;
  border: 2px solid;
  border-radius: 50%;
  position: absolute;
  z-index: 10;
  box-sizing: border-box;
}

.vue-flow__handle-left {
  color: #1fa2ff;
}


.vue-flow__handle-right {
  color: #fb0202;
}

.custom-handle:hover {
  background: #b8ababd3;
  cursor: crosshair;
}

.inputs, .outputs {
  position: absolute;
  height: calc(100% - 30px);
  width: 20px;
  top: 30px;
  pointer-events: none;
}

.inputs {
  left: 0;
}

.outputs {
  right: 0;
}
</style>