<script setup>
import { Handle } from '@vue-flow/core'
import { ResizeRotateNode } from '@vue-flow/resize-rotate-node'
import lifter from '@/assets/shelf.png'

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
    :selected="props.selected"
    :resize="props.resize"
    :rotate="props.rotate"
    :setRef="props.setRef"
  >
    <div class="node-wrapper">
      <div class="custom-node d":style="{ backgroundColor: calculateColorfromFloor(props.data.floor) }">
        <div class="node-title">{{ "货架" }}</div>
        <div class="floor-display">楼层: {{ props.data.floor }}</div>
        <div class="image-container">
          <img :src="lifter" alt="模块图示" class="node-image" />
        </div>
        <!-- 输入连接点 -->
        <Handle
          type="source"
          position="right"
          id="output-d"
          class="custom-handle output-handle"
        />

        <Handle
          type="target"
          position="left"
          id="input-d"
          class="custom-handle input-handle"
        />
      </div>
    </div>
  </ResizeRotateNode>
</template>

<style scoped>
.node-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  box-sizing: border-box;
  flex: 1 1 auto;
}

.custom-node.d {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: white;
  border: 2px solid #ff00d9;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  min-width: 50px;
  min-height: 50px;
}

.node-title {
  height: 20%;
  text-align: center;
  font-weight: bold;
  padding: 4px;
  background-color: #ffffff;
  box-sizing: border-box;
}

.image-container {
  height: 80%;
  width: 100%;
  overflow: hidden;
}

.node-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
</style>