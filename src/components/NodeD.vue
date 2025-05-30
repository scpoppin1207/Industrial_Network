<script setup>
import { Handle } from '@vue-flow/core'
import { ResizeRotateNode } from '@vue-flow/resize-rotate-node'
import lifter from '@/assets/shelf.png'

const props = defineProps(['id', 'data', 'selected', 'resize', 'rotate', 'setRef'])
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
      <div class="custom-node d">
        <div class="node-title">{{ "货架" }}</div>
        <div class="image-container">
          <img :src="lifter" alt="模块图示" class="node-image" />
        </div>
        <!-- 输入连接点 -->
        <Handle
          type="source"
          position="right"
          id="output-d"
          class="custom-handle"
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