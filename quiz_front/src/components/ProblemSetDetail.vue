<template>
  <div class="text-black p-4">
    <div v-if="loading">불러오는 중...</div>
    <div v-else-if="error" class="text-red-500 text-sm">{{ error }}</div>

    <div v-else-if="quizSet" class="space-y-4">
      <div>
        <div class="text-xs text-gray-500">ProblemSet #{{ quizSet.id }}</div>
        <h2 class="text-xl font-bold">{{ quizSet.title }}</h2>
        <p class="mt-2 text-sm text-gray-700 whitespace-pre-wrap">
          {{ quizSet.description }}
        </p>
      </div>
      <button
        v-if="canEdit"
        class="px-4 border rounded"
        @click="emit('edit', quizSet.id)"
      >
        수정
      </button>
      <div class="grid grid-cols-2 gap-2 text-sm">
        <div class="border rounded p-2">
          <div class="text-xs text-gray-500">작성자</div>
          <div class="font-medium">{{ quizSet.created_by_name ?? '-' }}</div>
        </div>
        <div class="border rounded p-2">
          <div class="text-xs text-gray-500">좋아요</div>
          <div class="font-medium">{{ quizSet.like_count ?? 0 }}</div>
        </div>
      </div>

      <!-- (선택) 미리보기 -->
      <div class="border rounded p-3">
        <div class="font-semibold mb-2">문제 수</div>
        {{ quizSet.problem_count }}
      </div>

      <div class="flex gap-2">
        <RouterLink :to="{ name: 'game', params: {'id':quizSet.id}}" class="flex-1 bg-blue-600 text-white py-2 rounded">
          Start
        </RouterLink >
        <button class="px-4 border rounded" @click="emit('close')">
          닫기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

const props = defineProps({
  quizsetid: { type: [String, Number], required: true },
})

const emit = defineEmits(['close', 'start', 'edit'])

const quizSet = ref(null)
const loading = ref(false)
const error = ref('')

const fetchDetail = async () => {
  loading.value = true
  error.value = ''
  quizSet.value = null


  try {
    const res = await axios.get(`${API_URL}/questions/problemsets/${props.quizsetid}/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    quizSet.value = res.data

    // ✅ 미리보기(선택): 문제 목록 API가 있으면 3개만 가져오기
    // 백엔드가 지원한다면:
    // const p = await axios.get(`${API_URL}/questions/problemsets/${props.quizsetid}/problems/`, ...)
    // preview.value = p.data.slice(0, 3)
  } catch (err) {
    console.error(err)
    error.value = '문제집 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

watch(() => props.quizsetid, fetchDetail, { immediate: true })

const canEdit = computed(() => {
  if (!quizSet.value) return false

  // ✅ 1) created_by(id)가 응답에 있으면 이게 제일 정확
  if (quizSet.value.created_by != null && accountStore.user?.pk != null) {
    return Number(quizSet.value.created_by) === Number(accountStore.user.pk)
  }
  return false
})

</script>