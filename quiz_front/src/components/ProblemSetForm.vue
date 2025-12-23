<template>

      <h1 class="mb-4 text-lg justiffont-semibold text-gray-900">
        문제집 생성
      </h1>

      <!-- 📄 폼 -->
      <form @submit.prevent="createProblemSets" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-900">
            Title
          </label>
          <input
            v-model.trim="title"
            type="text"
            required
            class="mt-2 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-900">
            Description
          </label>
          <input
            v-model.trim="description"
            type="text"
            required
            class="mt-2 block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>

        <button
          type="submit"
          class="w-full rounded-md bg-indigo-600 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          문제집 생성
        </button>
      </form>

      <!-- 생성 결과 (선택) -->
      <div v-if="problemSet" class="mt-4 text-sm text-gray-700">
        <h2 class="font-semibold">생성 완료</h2>
        <pre class="mt-2 rounded bg-gray-100 p-2 text-xs">
            {{ problemSet }}
        </pre>
      </div>

</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts'
  import { useRouter } from 'vue-router'
  import axios from 'axios'

  // API
  const API_URL = import.meta.env.VITE_REST_API_URL

  const emit = defineEmits(['close', 'created'])

  const accountStore = useAccountStore()

  const problemSet = ref(null)
  const title = ref(null)
  const description = ref(null)

  const createProblemSets = async () => {
    try {
      
      const res = await axios.post(
        `${API_URL}/questions/problemsets/`,
        {
          title: title.value,
          description: description.value
        },
        {
          headers: {
            Authorization: `Token ${accountStore.token}`
          }
        }
      )

      problemSet.value = res.data
      emit('created', res.data.id)

    } catch (err) {
      console.error(err)
    }
  }
</script>

<style scoped>

</style>