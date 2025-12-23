<template>
  <!-- ✅ 모달 전체 높이 제한 + 세로 레이아웃 -->
  <div class="text-black p-4 flex flex-col max-h-[70vh]">
    <!-- 헤더(고정) -->
    <div class="flex items-start justify-between gap-2 shrink-0">
      <div>
        <h2 class="text-lg font-bold">AI 코칭 결과</h2>
        <p class="text-xs text-gray-500 mt-1">
          오답 {{ meta?.count ?? 0 }}개 · 최근 {{ meta?.from_days ?? 7 }}일 · {{ meta?.model ?? '' }}
        </p>
      </div>
      <button class="px-3 py-1.5 border rounded text-sm" @click="emit('close')">
        닫기
      </button>
    </div>

    <!-- ✅ 본문(스크롤) -->
    <div class="border rounded p-3 bg-white mt-3 flex-1 overflow-y-auto">
      <div class="text-sm whitespace-pre-wrap leading-relaxed">
        {{ feedback }}
      </div>
    </div>

    <!-- 하단 버튼(고정) -->
    <div class="flex gap-2 mt-3 shrink-0">
      <button class="flex-1 bg-blue-600 text-white py-2 rounded" @click="emit('retry')">
        다시 생성
      </button>
      <button class="px-4 border rounded" @click="emit('close')">
        닫기
      </button>
    </div>

    <p class="text-[11px] text-gray-500 leading-relaxed mt-3 shrink-0">
      ※ AI 피드백은 참고용입니다. 최종 판단은 문제/해설을 직접 확인하세요.
    </p>
  </div>
</template>

<script setup>
defineProps({
  feedback: { type: String, default: '' },
  meta: { type: Object, default: () => ({}) },
})
const emit = defineEmits(['close', 'retry'])
</script>

<style scoped>

</style>