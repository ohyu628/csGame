<template>
  <div class="w-full h-full min-h-0 flex flex-col text-black">
    <!-- ✅ 패널(위쪽, 남은 공간) -->
    <div class="pixel-panel flex-1 min-h-0 flex flex-col">
      <div class="pixel-panel__content flex-1 min-h-0 overflow-auto flex flex-col items-center">
        <div class="m-4 font-bold text-xl text-center">
          내가 만든 문제집 목록
        </div>

        <ul class="w-full max-w-[360px]">
          <li
            v-for="quizset in quizSets"
            :key="quizset.id"
            class="cursor-pointer hover:bg-gray-50 text-center"
            @click="openDetail(quizset.id)"
          >
            {{ quizset.title }} like: {{ quizset.like_count }}
            <hr />
          </li>
        </ul>
      </div>
    </div>

    <!-- ✅ 버튼(패널 밖, 맨 아래, 중앙 정렬) -->
    <div class="shrink-0 w-full mt-4 flex justify-center pb-3">
      <button
        @click="openModal"
        class="px-4 py-2 bg-blue-500 text-white rounded"
      >
        문제집 생성
      </button>
    </div>

    <!-- ✅ 모달 -->
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
import QuizDetail from '@/components/QuizDetail.vue'   // ✅ 추가

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const modal = useModalStore()

const quizSets = ref([])
const currentQuizsetId = ref(null)

// ✅ 모달 교체
const modalView = shallowRef(ProblemSetForm)
const modalProps = ref({})

// ✅ 모달별 이벤트 라우팅 (UserMode랑 동일하게)
const extraListeners = computed(() => {
  const name = modalView.value?.__name

  if (name === 'ProblemSetCreate' || name === 'ProblemSetDetail') {
    return {
      updated: onUpdated,
      goCreateQuiz: onGoCreateQuiz,
      edit: onEditProblemSet,
      openQuizDetail: onOpenQuizDetail, // ✅ 추가
    }
  }

  if (name === 'QuizCreate') {
    return { done: backToProblemSetCreate }
  }

  if (name === 'QuizDetail') {
    return {
      back: backToProblemSetCreate,
      saved: backToProblemSetCreate,
      deleted: backToProblemSetCreate,
      close: closeModal, // 선택: 닫기 버튼 처리용
    }
  }

  return {}
})

// ✅ 목록 조회
const getQuizSets = async () => {
  try {
    const res = await axios.get(`${API_URL}/questions/problemsets/`, {
      headers: { Authorization: `Token ${accountStore.token}` },
    })
    quizSets.value = res.data
  } catch (err) {
    console.error(err)
  }
}

// ✅ 생성 모달
const openModal = () => {
  modalView.value = ProblemSetForm
  modalProps.value = {}
  modal.open(1)
}

// ✅ 생성 완료 → 관리 모달
const onCreated = (createdId) => {
  currentQuizsetId.value = createdId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: createdId }
}

// ✅ 수정 저장 완료 시 목록 갱신
const onUpdated = () => {
  getQuizSets()
}

const closeModal = () => modal.close()

// ✅ 문제 추가로 이동
const onGoCreateQuiz = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = QuizCreate
  modalProps.value = { quizsetid: quizsetId }
}

// ✅ 퀴즈 생성 완료 → 다시 문제집 관리로
const backToProblemSetCreate = () => {
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: currentQuizsetId.value }
}

// ✅ 상세에서 수정 버튼 눌렀을 때 → 관리 화면으로
const onEditProblemSet = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetCreate
  modalProps.value = { quizsetid: quizsetId }
}

// ✅ QuizList에서 quiz 클릭 → QuizDetail로 전환
const onOpenQuizDetail = ({ quizId, quizSetId }) => {
  currentQuizsetId.value = quizSetId
  modalView.value = QuizDetail
  modalProps.value = { quizid: quizId, quizsetid: quizSetId }
}

// ✅ 목록 클릭 → 상세 모달
const openDetail = (quizsetId) => {
  currentQuizsetId.value = quizsetId
  modalView.value = ProblemSetDetail
  modalProps.value = { quizsetid: quizsetId }
  modal.open(1)
}

onMounted(getQuizSets)
</script>
