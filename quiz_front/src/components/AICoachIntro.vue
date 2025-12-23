<template>
  <div class="text-black p-4 space-y-4">
    <h2 class="text-lg font-bold">AI 코칭 안내</h2>

    <div class="text-sm text-gray-700 space-y-2 whitespace-pre-wrap">
      <p>• 최근 7일 내 오답(최대 30개)을 기반으로 학습 피드백을 생성합니다.</p>
      <p>• 생성된 피드백은 참고용이며, 최종 판단은 본인이 확인해야 합니다.</p>
      <p>• 네트워크 상황에 따라 요청 시간이 길어질 수 있습니다.</p>
      <p class="text-red-600 font-medium">※ 오답이 없으면 코칭이 생성되지 않을 수 있습니다.</p>
    </div>

    <!-- ✅ 로딩 표시 -->
    <div v-if="loading" class="border rounded p-3 bg-gray-50">
      <p class="text-sm font-medium">
        코칭 생성 중<span class="inline-block w-[24px]">{{ dots }}</span>
      </p>
      <p class="text-xs text-gray-500 mt-1">잠시만 기다려 주세요.</p>
      <!-- 나중에 여기 스프라이트 로딩으로 교체하면 됨 -->
    </div>

    <p v-if="error" class="text-sm text-red-600 whitespace-pre-wrap">
      {{ error }}
    </p>

    <div class="flex gap-2">
      <button
        class="flex-1 bg-blue-600 text-white py-2 rounded disabled:opacity-50"
        :disabled="loading"
        @click="emit('start')"
      >
        코칭 진행!
      </button>
      <button
        class="px-4 border rounded disabled:opacity-50"
        :disabled="loading"
        @click="emit('close')"
      >
        취소
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
const emit = defineEmits(['start', 'close'])

const dots = ref('')
let timer = null

const startDots = () => {
  // 이미 돌고 있으면 중복 방지
  if (timer) return

  let n = 0
  timer = setInterval(() => {
    n = (n % 3) + 1 // 1~3
    dots.value = '.'.repeat(n)
  }, 350)
}

const stopDots = () => {
  if (timer) clearInterval(timer)
  timer = null
  dots.value = ''
}

watch(
  () => props.loading,
  (isLoading) => {
    if (isLoading) startDots()
    else stopDots()
  },
  { immediate: true }
)

onBeforeUnmount(() => stopDots())
</script>

<style scoped>
</style>
