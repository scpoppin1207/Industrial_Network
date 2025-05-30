<script setup>
import { Handle, Position } from '@vue-flow/core'
import { ResizeRotateNode } from '@vue-flow/resize-rotate-node'
import { ref, watchEffect} from 'vue'
import my_transfer from '@/assets/transfer.png'
// 获取 props
const props = defineProps(['id', 'data', 'selected', 'resize', 'rotate', 'setRef'])


</script>

<template>
  <ResizeRotateNode
    :id="props.id"
    :data="props.data"
  >
   <div class="node-wrapper" >
    <div class="custom-node a">
      <div class="node-title">{{ "输送机" }}</div>
      <div class="image-container">
          <img :src="my_transfer" alt="模块图示" class="node-image" />
        </div>

      <!-- 输入连接点 -->
      <Handle
        type="target"
        position="left"
        id="input-a"
        class="custom-handle"
      />
      <!-- 输出连接点 -->
      <Handle
        type="source"
        position="right"
        id="output-a"
        class="custom-handle"
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

.custom-handle {
  width: 24px;
  height: 24px;
  background: white;
  border: 2px solid #2196F3;
  border-radius: 50%;
  box-sizing: border-box;
}

.custom-handle:hover {
  background: #2196F3;
  cursor: crosshair;
}
</style>