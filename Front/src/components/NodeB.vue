<script setup>
import { Handle, Position } from '@vue-flow/core'
import { ResizeRotateNode } from '@vue-flow/resize-rotate-node'
import transplant from '@/assets/transplant.png'

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
      <div class="custom-node b">
        <div class="node-title">{{ "移栽机" }}</div>
        <div class="floor-display">楼层: {{ props.data.floor }}</div>
        <div class="image-container">
          <img :src="transplant" alt="模块图示" class="node-image" />
        </div>
        <!-- 输入连接点 -->
        <Handle
          type="target"
          position="left"
          id="input-b"
          class="custom-handle input-handle"
        />
        <!-- 输出连接点1 -->
        <Handle
          type="source"
          position="top"
          id="output-b1"
          class="custom-handle output-handle"
        />
        <!-- 输出连接点2 -->
        <Handle
          type="source"
          position="bottom"
          id="output-b2"
          class="custom-handle output-handle"
        />
         <!-- 输出连接点2 -->
        <Handle
          type="source"
          position="right"
          id="output-b3"
          class="custom-handle output-handle"
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

.custom-node.b {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: white;
  border: 2px solid #FF9800;
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