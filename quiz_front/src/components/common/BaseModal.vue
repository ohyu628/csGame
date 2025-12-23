<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- 배경 -->
    <div class="absolute inset-0 bg-black/50" @click="emitClose" />

    <!-- 모달 박스 -->
<!-- 모달 박스 -->
<div
  class="relative z-10
         w-[calc(100%-2rem)] max-w-[400px]
         box-border overflow-hidden
         pixel-panel"
  @click.stop
>
  <!-- 닫기 버튼 -->
  <button
    class="absolute top-2 right-2 text-gray-400 hover:text-black"
    @click="emitClose"
  >
    ✕
  </button>

  <!-- ⭐ 내용 삽입 영역 -->
  <div class="pixel-panel__content">
    <slot />
  </div>
</div>

  </div>
</template>

<script setup>
const emit = defineEmits(['close'])
const emitClose = () => emit('close')
</script>