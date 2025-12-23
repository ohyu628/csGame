<template>
  <div>
    <h1>맵 문제집 목록</h1>

    <ul>
      <li
        v-for="ps in problemSets.problem_sets"
        :key="ps.id"
        class="cursor-pointer hover:underline"
        @click="openDetail(ps)"
      >
        {{ ps.title }}
      </li>
    </ul>

    <!-- ✅ BaseModal: axios로 받은 detail만 표시 -->
    <div class="text-black">
    <BaseModal v-if="modal.isOpen" @close="closeDetail">

      제목: {{ selected.title }} <br/>
      설명: {{ selected.description }}<br/>
      <RouterLink :to="{ name: 'game', params: { id: selected.id }}">게임 시작</RouterLink>

    </BaseModal>
    </div>
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

const selected = ref(null)

const getProblemSets = async () => {
  const res = await axios.get(`${API_URL}/game/maps/${mapId.value}`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  problemSets.value = res.data
}

const openDetail = async (data) => {
  selected.value = data
  modal.open()
}

const closeDetail = () => {
  modal.close()
}

onMounted(getProblemSets)
</script>
