<template>
  <div class="h-full w-full min-h-0 flex flex-col text-black">
    <!-- 전체 패널(카드) -->
    <div class="flex h-full">
    <div class="pixel-panel w-full mx-auto flex-1 min-h-0 flex flex-col">
    <!-- <div class="pixel-panel m-2 w-full max-w-[420px] flex-1 min-h-0 flex flex-col"> -->
      <!-- 헤더(고정) -->
      <div class="shrink-0">
        <div class="flex justify-center tracking-wide mt-2">
          <h1>유저 모드 페이지</h1>
        </div>

        <div class="flex justify-end mr-4">
          <button @click="openModal" class="text-xs">
            문제집 생성
          </button>
        </div>
      </div>

      <!-- 리스트(남은 영역 전부 + 여기만 스크롤) -->
      <div class="pixel-panel__content flex-1 min-h-0 overflow-y-auto">
        <ul>
          <li
            v-for="quizset in pagedQuizsets"
            :key="quizset.id"
            class="cursor-pointer hover:bg-gray-50"
            @click="openDetail(quizset.id)"
          >
            제목: {{ quizset.title }} <br />
            좋아요: {{ quizset.like_count }} | 작성자: {{ quizset.created_by_name }}
            <hr />
          </li>
        </ul>
      </div>

      <!-- 페이지네이션(고정) -->
      <div v-if="totalPages > 1" class="shrink-0 flex items-center justify-between gap-2 px-2 py-2">
        <button
          class="px-3 py-1 border rounded disabled:opacity-40"
          :disabled="page === 1"
          @click="page--"
        >
          이전
        </button>

        <div class="text-sm">
          {{ page }} / {{ totalPages }}
        </div>

        <button
          class="px-3 py-1 border rounded disabled:opacity-40"
          :disabled="page === totalPages"
          @click="page++"
        >
          다음
        </button>
      </div>
    </div>
    </div>

    <!-- 모달 -->
    <BaseModal v-if="modal.isOpen" @close="closeModal">
      <component
        :is="modalView"
        v-bind="modalProps"
        @created="onCreated"
        @close="closeModal"
        v-on="extraListeners"
      />
    </BaseModal>
  </div>
</template>


<script setup>
import { ref, onMounted, shallowRef, computed } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useModalStore } from '@/stores/modal'
import axios from 'axios'
import BaseModal from '@/components/common/BaseModal.vue'
import ProblemSetForm from '@/components/ProblemSetForm.vue'
import ProblemSetCreate from '@/components/ProblemSetCreate.vue'
import QuizCreate from '@/components/QuizCreate.vue'
import ProblemSetDetail from '@/components/ProblemSetDetail.vue'
import QuizDetail from '@/components/QuizDetail.vue'


const API_URL = import.meta.env.VITE_REST_API_URL
const modal = useModalStore()
const accountStore = useAccountStore()

const currentQuizsetId = ref(null)

const quizsets = ref([])

// ✅ 모달 내용 교체용
const modalView = shallowRef(ProblemSetForm)
const modalProps = ref({})

const extraListeners = computed(() => {
  const name = modalView.value?.__name   // ✅ 컴포넌트 이름으로 판별
  ////나중에 문제 가능 표식/////////////////
  if (name === 'ProblemSetCreate' || name === 'ProblemSetDetail') {
    return { updated: onUpdated, goCreateQuiz: onGoCreateQuiz, edit: onEditProblemSet, openQuizDetail: onOpenQuizDetail,  }
  }
  
  if (name === 'QuizCreate') {
    return { done: backToProblemSetCreate }
  }

  if (name === 'QuizDetail') {
    return { back: backToProblemSetCreate, saved: backToProblemSetCreate, deleted: backToProblemSetCreate }
  }

  return {}
})
  
const getProblemSets = async () => {
  const res = await axios.get(`${API_URL}/game/users/problemsets/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  quizsets.value = res.data
  page.value = 1
}

const onOpenQuizDetail = ({ quizId, quizSetId }) => {
  currentQuizsetId.value = quizSetId
  modalView.value = QuizDetail
  modalProps.value = { quizid: quizId, quizsetid: quizSetId }
}

// ✅ 생성 버튼 → 생성 폼 모달
const openModal = () => {
  modalView.value = ProblemSetForm
  modalProps.value = {}
  modal.open(1)
}

// ✅ 생성 성공 → 디테일/수정 모달로 전환 (props 이름 맞추기!)
const onCreated = (createdId) => {
  currentQuizsetId.value = createdId 
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: createdId } // ✅ 여기!
}

// ✅ 디테일에서 저장 완료 시 목록 갱신 (선택)
const onUpdated = () => {
  getProblemSets()
}

const closeModal = () => modal.close()

const onGoCreateQuiz = (quizsetId) => {
  console.log('modalView=', modalView.value, 'modalProps=', modalProps.value)
  console.log('onGoCreateQuiz fired:', quizsetId)
  currentQuizsetId.value = quizsetId
  modalView.value = QuizCreate
  modalProps.value = { quizsetid: quizsetId } // ✅ QuizCreate가 받을 props
}

const backToProblemSetCreate = () => {
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: currentQuizsetId.value }
}

const onEditProblemSet = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: quizsetId }
}

const openDetail = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetDetail
  modalProps.value = { quizsetid: quizsetId }
  modal.open(1)
}

const page = ref(1)
const pageSize = 8

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(quizsets.value.length / pageSize))
})

const pagedQuizsets = computed(() => {
  const start = (page.value - 1) * pageSize
  return quizsets.value.slice(start, start + pageSize)
})



onMounted(getProblemSets)
</script>
