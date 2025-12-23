<template>
  <div>
    <h1>맵 문제집 목록</h1>

    <ul>
      <li
        v-for="ps in problemSets.problem_sets"
        :key="ps.id"
        class="cursor-pointer hover:underline"
        @click="openDetail(ps.id)"
      >
        {{ ps.title }}
      </li>
    </ul>

    <!-- ✅ BaseModal: axios로 받은 detail만 표시 -->
    <BaseModal v-if="modal.isOpen" @close="closeDetail">
      <h2 class="text-lg font-bold">{{ detail?.title }}</h2>
      <p class="mt-2 text-sm text-gray-600">{{ detail?.description }}</p>

      <div class="mt-3 text-sm space-y-1">
        <div>문제 수: {{ detail?.problem_count }}</div>
        <div>작성자: {{ detail?.created_by_name }}</div>
      </div>

      <button
        class="mt-4 w-full bg-gray-800 text-white py-2 rounded"
        @click="closeDetail"
      >
        닫기
      </button>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { useRoute } from 'vue-router'
import axios from 'axios'
import BaseModal from '@/components/common/BaseModal.vue'
import { useModalStore } from '@/stores/modal'

const API_URL = import.meta.env.VITE_REST_API_URL

const accountStore = useAccountStore()
const modal = useModalStore()
const route = useRoute()

const mapId = ref(route.params.mapid)
const problemSets = ref([])

const detail = ref(null)

const getProblemSets = async () => {
  const res = await axios.get(`${API_URL}/game/maps/${mapId.value}`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  problemSets.value = res.data
}

// ✅ watch 없음: 클릭하면 상세 요청 → detail 채움 → 모달 오픈
const openDetail = async (id) => {
  const res = await axios.get(`${API_URL}/maps/${id}/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  detail.value = res.data
  modal.open(id)
}

const closeDetail = () => {
  modal.close()
  detail.value = null
}

onMounted(getProblemSets)
</script>
