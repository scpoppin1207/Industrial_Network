<template>
<router-view />
</template>


<script setup>
import { ref } from 'vue'
import EntrySelector from './components/EntrySelector.vue'
import SystemDesigner from './components/SystemDesigner.vue'
const entry = ref('')

</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

body {
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  background-attachment: fixed;
  min-height: 100vh;
}

</style>