<template>
  <div class="text-black">
    <h3 class="font-semibold mb-2">퀴즈 리스트</h3>

    <p v-if="loading" class="text-sm">불러오는 중...</p>
    <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>

    <ul v-else class="space-y-1">
      <li
        v-for="quiz in quizzes"
        :key="quiz.id"
        class="border rounded px-2 py-2 hover:bg-gray-50 cursor-pointer"
        @click="onSelect(quiz)"
      >
        <span v-if="quiz?.id" class="hover:underline">
          {{ quiz.question }}
        </span>
        <span v-else class="text-gray-500 text-sm">잘못된 데이터</span>
      </li>
    </ul>

    <p v-if="!loading && !error && quizzes.length === 0" class="text-sm text-gray-600 mt-2">
      아직 등록된 문제가 없습니다.
    </p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import axios from 'axios'

const props = defineProps({
  quizSetId: { type: [Number, String], required: true },
})

const emit = defineEmits(['select'])

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

const quizzes = ref([])
const loading = ref(false)
const error = ref('')

const getQuiz = async () => {
  if (!props.quizSetId) return
  loading.value = true
  error.value = ''

  try {
    const res = await axios.get(
      `${API_URL}/questions/problemsets/${props.quizSetId}/problems/`,
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )
    quizzes.value = res.data
  } catch (err) {
    console.error(err)
    quizzes.value = []
    error.value = '퀴즈 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

const onSelect = (quiz) => {
  if (!quiz?.id) return
  emit('select', quiz.id)
}

watch(() => props.quizSetId, getQuiz, { immediate: true })
</script>
