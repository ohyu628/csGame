<template>
  <div class="h-full w-full min-h-0 flex flex-col gap-2">
    <!-- 상단 패널 -->
    <div class="pixel-panel flex-[7] min-h-0">
      <div class="pixel-panel__content h-full min-h-0 overflow-hidden">
        <h1 class="text-black text-lg font-bold mb-3">AI 모드</h1>
      </div>
    </div>

    <!-- 하단 패널 -->
    <div class="pixel-panel m-2 flex-[3] min-h-0">
      <div class="pixel-panel__content h-full min-h-0 overflow-hidden">
        <h1 class="text-black text-lg font-bold mb-3">대화창?</h1>
      </div>
    </div>

    <!-- 버튼은 맨 아래 고정(줄어들지 않게) -->
    <div class="m-2 shrink-0">
      <button
        class="w-full bg-blue-600 text-white py-2 rounded"
        @click="openCoachingIntro"
      >
        AI 코칭!
      </button>
    </div>

    <!-- 모달 -->
    <BaseModal v-if="modal.isOpen" @close="closeModal">
      <component
        :is="modalView"
        v-bind="modalProps"
        @close="closeModal"
        v-on="extraListeners"
      />
    </BaseModal>
  </div>
</template>

<script setup>
import { shallowRef, ref, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useModalStore } from '@/stores/modal'

import BaseModal from '@/components/common/BaseModal.vue'
import AICoachIntro from '@/components/AICoachIntro.vue'
import AIFeedbackModal from '@/components/AIFeedbackModal.vue'

const API_URL = import.meta.env.VITE_REST_API_URL
const accountStore = useAccountStore()
const modal = useModalStore()

const modalView = shallowRef(AICoachIntro)
const modalProps = ref({
  loading: false,
  error: '',
})

const feedbackState = ref({
  feedback: '',
  meta: { count: 0, from_days: 7, model: '' },
})

const extraListeners = computed(() => {
  if (modalView.value === AICoachIntro) {
    return { start: onStartCoaching }
  }
  if (modalView.value === AIFeedbackModal) {
    return { retry: onRetry }
  }
  return {}
})

const openCoachingIntro = () => {
  modalView.value = AICoachIntro
  modalProps.value = { loading: false, error: '' }
  modal.open(1)
}

const closeModal = () => {
  modal.close()
  // 닫을 때 상태 정리(원하면)
  modalProps.value = { loading: false, error: '' }
  feedbackState.value = { feedback: '', meta: { count: 0, from_days: 7, model: '' } }
}

// ✅ "AICoachingIntro -> start" 누르면: Intro는 로딩 상태로 유지 + AIMode에서 axios 실행
const onStartCoaching = async () => {
  // Intro 모달 그대로 두고 로딩만 켬
  modalProps.value = { ...modalProps.value, loading: true, error: '' }

  try {
    const res = await axios.post(
      `${API_URL}/ai/feedback/`, // 네 DRF 엔드포인트
      { days: 7, limit: 30 },
      { headers: { Authorization: `Token ${accountStore.token}` } }
    )

    const feedback = (res.data.feedback ?? '').trim()

    // 오답 없음 같은 케이스 처리 (서버가 detail 주는 패턴)
    if (!feedback) {
      modalProps.value = {
        ...modalProps.value,
        loading: false,
        error: res.data.detail || '피드백이 비어 있습니다.',
      }
      return
    }

    // ✅ 응답 오면: 모달 컴포넌트를 결과 모달로 교체
    feedbackState.value = {
      feedback,
      meta: {
        count: res.data.count ?? 0,
        from_days: res.data.from_days ?? 7,
        model: res.data.model ?? '',
      },
    }

    modalView.value = AIFeedbackModal
    modalProps.value = {
      feedback: feedbackState.value.feedback,
      meta: feedbackState.value.meta,
    }
  } catch (e) {
    console.error(e)
    modalProps.value = {
      ...modalProps.value,
      loading: false,
      error:
        e?.response?.data?.detail ||
        '코칭 생성에 실패했습니다.',
    }
  } finally {
    // Intro 화면일 때만 로딩 끄기 (이미 결과로 넘어갔으면 의미 없음)
    if (modalView.value?.__name === 'AICoachIntro') {
      modalProps.value = { ...modalProps.value, loading: false }
    }
  }
}

const onRetry = () => {
  // 결과 화면에서 다시 누르면 인트로로 돌아가서 바로 재시도할 수도 있음
  modalView.value = AICoachIntro
  modalProps.value = { loading: false, error: '' }
  onStartCoaching()
}
</script>



<style scoped>

</style>