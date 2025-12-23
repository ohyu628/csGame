<template>
  <div class="h-screen flex justify-center bg-neutral-900 overflow-x-auto">
    <div class="w-full max-w-[420px] min-w-[420px] h-screen bg-amber-50 overflow-hidden">
      <RouterView class="h-full" />
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style scoped>

</style>
