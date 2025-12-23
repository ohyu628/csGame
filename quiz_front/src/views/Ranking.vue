<template>
  <div class="pixel-panel w-full text-black">
    <div v-if="rankData" class="pixel-panel__content flex flex-col items-center">
      <div class="w-full text-center text-xl font-bold mb-4">
        Ranking Board
      </div>

      <ul class="w-full max-w-[360px] flex flex-col items-center gap-2">
        <li
          v-for="rank in rankData.items"
          :key="rank.user_id"
          class="w-full flex items-center justify-between px-3 py-2 bg-white/70 rounded border"
        >
          <span class="w-10 text-center font-bold">{{ rank.rank }}</span>
          <span class="flex-1 text-center">{{ rank.username }}</span>
          <span class="w-16 text-center">Lv {{ rank.level }}</span>
          <span class="w-24 text-right">{{ rank.total_experience }}</span>
        </li>
      </ul>
    </div>

    <div v-else class="pixel-panel__content text-center text-gray-500">
      로딩중...
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted} from 'vue'
import { useAccountStore } from '@/stores/accounts'


const accountStore = useAccountStore()
const API_URL = import.meta.env.VITE_REST_API_URL


const rankData = ref(null)

const getRank = async () => {
  const res = await axios.get(`${API_URL}/profile/ranking/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  rankData.value = res.data
}

onMounted(getRank)
</script>

<style scoped>

</style>