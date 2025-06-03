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

</style>