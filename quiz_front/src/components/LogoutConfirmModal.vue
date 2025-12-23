<template>
  <div class="text-black p-4 space-y-4">
    <h2 class="text-lg font-bold">메뉴</h2>

    <p class="text-sm text-gray-700">
      로그아웃 하시겠습니까?
    </p>

    <div class="flex gap-2">
      <button
        class="flex-1 bg-red-600 text-white py-2 rounded"
        @click="emit('logout')"
      >
        로그아웃
      </button>
      <button
        class="px-4 border rounded"
        @click="emit('close')"
      >
        취소
      </button>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close', 'logout'])
</script>
