<script setup>
import { Handle, Position} from '@vue-flow/core'
import { ResizeRotateNode } from '@vue-flow/resize-rotate-node'
import my_transfer from '@/assets/transfer.png'
const props = defineProps(['id', 'data', 'selected', 'resize', 'rotate', 'setRef'])
const calculateColorfromFloor = (floor) => {
  // 根据楼层计算颜色,随着楼层升高从白色到灰色渐变
  const maxFloor = 10; // 假设最大楼层为10
  const ratio = Math.min(floor / maxFloor, 1); // 确保比例在0到1之间
  const r = Math.floor(255 * (1 - ratio)); // 红色从255降到0
  const g = Math.floor(255 * (1 - ratio)); // 绿色从255降到0
  const b = Math.floor(255 * (1 - ratio)); // 蓝色从255降到0
  return `rgb(${r}, ${g}, ${b})`; // 返回RGB颜色字符串
}


</script>

<template>
  <ResizeRotateNode
    :id="props.id"
    :data="props.data"
  >
   <!-- 修改绑定 -->
   <div class="node-wrapper" :data-node-id="props.id">
    <div class="custom-node a" :style="{ backgroundColor: calculateColorfromFloor(props.data.floor) }">
      <div class="node-title">{{ "输送机" }}</div>
      <div class="floor-display">楼层: {{ props.data.floor }}</div>
      <!-- 新增属性展示 -->
      <div class="property-display">速度: {{ props.data.speed }}</div>
      <div class="property-display">长度: {{ props.data.length }}</div>
      <div class="image-container">
          <img :src="my_transfer" alt="模块图示" class="node-image" />
        </div>

      <!-- 输入连接点 -->
      <Handle
        type="target"
        position="left"
        id="input-a"
        class="custom-handle input-handle"
      />
      <!-- 输出连接点 -->
      <Handle
        type="source"
        position="right"
        id="output-a"
        class="custom-handle output-handle"
      />
    </div>
   </div>
  </ResizeRotateNode>
</template>

<style scoped>

/* 关键样式设置 */
:deep([data-moveable-id]) {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: stretch !important; /* 垂直拉伸 */
  justify-content: stretch !important; /* 水平拉伸 */
}

.node-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  box-sizing: border-box;
  flex: 1 1 auto;
}

.custom-node.a {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: white;
  border: 2px solid #4CAF50;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  min-width: 50px; /* 最小宽度 */
  min-height: 50px; /* 最小高度 */
}

.node-title {
  height: 20%;
  text-align: center;
  font-weight: bold;
  padding: 4px;
  background-color: #ffffff;
  box-sizing: border-box;
}

/* 图片容器占 80% */
.image-container {
  height: 80%;
  width: 100%;
  overflow: hidden;
}

/* 图片填满容器 */
.node-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


.node-title {
  font-weight: bold;
  margin-bottom: 8px;
  text-align: center;
  user-select: text;
}


.input-handle {
  width: 24px;
  height: 24px;
  background: white;
  border: 2px solid #008cff;
  border-radius: 50%;
  box-sizing: border-box;
}

.output-handle {
  width: 24px;
  height: 24px;
  background: white;
  border: 2px solid #ff0000;
  border-radius: 50%;
  box-sizing: border-box;
}


.custom-handle:hover {
  background: #b8ababd3;
  cursor: crosshair;
}

.floor-display {
  text-align: center;
  font-size: 14px;
  margin: 8px 0;
  color: #555;
}

/* 新增属性展示样式 */
.property-display {
  text-align: center;
  font-size: 14px;
  margin: 4px 0;
  color: #333;
}
</style>