<template>
  <div class="text-black">
    <div v-if="stats">
    <div class="pixel-panel max-w-[250px] text-sm">
      <div class="pixel-panel__content">
      
      <span class="font-bold flex justify-center">
        LV. {{ stats.profile.level }}  {{ stats.profile.username }} 
      </span><br/>
      EXP {{ stats.profile.exp }} / {{ stats.profile.max_exp }}
      <br/> <hr/>
      <!-- {{ stats.stats }} -->
      <span class="m-1 font-bold flex justify-center">
        통계
      </span>
      푼 문제: {{ stats.stats.total_solved }} <br/>
      맞춘 문제: {{ stats.stats.total_correct }} <br/>
      정확도: {{ stats.stats.accuracy_pct }} %
      <hr/>
      <span class="m-1 font-bold flex justify-center">
        숙련도
      </span>
      <div v-for="category in stats.category_stats" :key="category.category_id">
        
        <span>{{ category.category_name }}</span>: {{ category.proficiency_score }}
      </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/accounts";
import axios from 'axios'
import { ref, onMounted } from 'vue'

const accountStore = useAccountStore()

const API_URL = import.meta.env.VITE_REST_API_URL

const stats = ref(null)


const getStatus = async () => {
  const res = await axios.get(`${API_URL}/profile/status/`, {
    headers: { Authorization: `Token ${accountStore.token}` },
  })
  stats.value = res.data
}

onMounted(getStatus)
</script>

<style scoped>

</style>