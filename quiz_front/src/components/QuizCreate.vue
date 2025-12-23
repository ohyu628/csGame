<template>
  <div class="text-black h-full max-h-[70vh] flex flex-col px-2">
    <!-- 제목 (고정) -->
    <h1 class="text-base font-semibold mb-3 shrink-0">
      퀴즈 생성
    </h1>

    <!-- 🔽 스크롤 영역 -->
    <div class="flex-1 max-h-[50vh] overflow-y-auto pr-1">
      <form @submit.prevent="createQuiz" class="space-y-3">
        <!-- 질문 -->
        <div>
          <label class="block text-xs font-medium mb-1">문제</label>
          <input
            v-model.trim="form.question"
            required
            class="w-full border rounded px-2 py-1.5 text-sm"
          />
        </div>

        <!-- 선택지 -->
        <div v-for="i in 4" :key="i">
          <label class="block text-xs font-medium mb-1">선택지 {{ i }}</label>
          <input
            v-model.trim="form[`choice${i}`]"
            required
            class="w-full border rounded px-2 py-1.5 text-sm"
          />
        </div>

        <!-- 정답 -->
        <div>
          <label class="block text-xs font-medium mb-1">정답</label>
          <select
            v-model.number="form.answer"
            required
            class="w-full border px-2 py-1.5 text-sm"
          >
            <option disabled value="">선택</option>
            <option v-for="n in 4" :key="n" :value="n">
              {{ n }}번
            </option>
          </select>
        </div>

        <!-- 난이도 -->
        <div>
          <label class="block text-xs font-medium mb-1">난이도</label>
          <select
            v-model="form.difficulty"
            required
            class="w-full border px-2 py-1.5 text-sm"
          >
            <option disabled value="">선택</option>
            <option value="easy">easy</option>
            <option value="medium">medium</option>
            <option value="hard">hard</option>
          </select>
        </div>

        <!-- 해설 -->
        <div>
          <label class="block text-xs font-medium mb-1">해설</label>
          <textarea
            v-model.trim="form.explanation"
            class="w-full border rounded px-2 py-1.5 text-sm"
            rows="3"
          />
        </div>

        <!-- 제출 버튼 -->
        <button
          type="submit"
          class="w-full bg-blue-500 text-white py-2 rounded sticky bottom-0"
        >
          생성
        </button>

        <p v-if="error" class="text-red-500 text-xs">{{ error }}</p>

        <!-- 하단 버튼(선택): 닫기 -->
        <button
          type="button"
          class="w-full border py-2 rounded"
          @click="emit('close')"
        >
          닫기
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()

// ✅ 모달에서 주입 받는 문제집 id
const props = defineProps({
  quizsetid: {
    type: [String, Number],
    required: true,
  },
})

const emit = defineEmits(['done', 'close'])

const error = ref('')

const form = reactive({
  question: '',
  choice1: '',
  choice2: '',
  choice3: '',
  choice4: '',
  answer: '',        // v-model.number로 number가 들어옴
  difficulty: '',    // easy | medium | hard
  explanation: '',
})

const resetForm = () => {
  Object.assign(form, {
    question: '',
    choice1: '',
    choice2: '',
    choice3: '',
    choice4: '',
    answer: '',
    difficulty: '',
    explanation: '',
  })
}

const createQuiz = async () => {
  error.value = ''

  // 🔒 프론트 1차 검증
  if (![1, 2, 3, 4].includes(form.answer)) {
    error.value = '정답은 1~4번 중에서 선택해야 합니다.'
    return
  }
  if (!['easy', 'medium', 'hard'].includes(form.difficulty)) {
    error.value = '난이도를 선택해주세요.'
    return
  }

  try {
    await axios.post(
      `${API_URL}/questions/problemsets/${props.quizsetid}/problems/`,
      {
        question: form.question,
        choice1: form.choice1,
        choice2: form.choice2,
        choice3: form.choice3,
        choice4: form.choice4,
        answer: form.answer,
        difficulty: form.difficulty,
        explanation: form.explanation,
      },
      {
        headers: { Authorization: `Token ${accountStore.token}` },
      }
    )

    resetForm()
    alert('퀴즈 생성 완료')

    // ✅ 부모(UserMode)에게 "이제 ProblemSetCreate로 돌아가" 신호
    emit('done')
  } catch (err) {
    console.error(err)
    error.value = '퀴즈 생성에 실패했습니다.'
  }
}
</script>

<style scoped>
</style>
