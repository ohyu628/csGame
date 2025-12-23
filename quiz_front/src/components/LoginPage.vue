<template>



    <!-- 카드 -->
    <div class="relative justify-center w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl ">
      <!-- 닫기 버튼 -->
      <button
        @click="close"
        class="absolute right-4 top-4 text-gray-400 hover:text-gray-600"
        aria-label="Close"
      >
        ✕
      </button>

      <!-- 로고 & 타이틀 -->
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900">
          Sign in to your account
        </h2>
      </div>

      <!-- 로그인 폼 -->
      <div class="mt-8">
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-900">
              ID
            </label>
            <div class="mt-2">
              <input
                v-model.trim="username"
                id="username"
                type="text"
                autocomplete="username"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-900">
              Password
            </label>
            <div class="mt-2">
              <input
                v-model.trim="password"
                id="password"
                type="password"
                autocomplete="current-password"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          <button
            type="submit"
            class="w-full rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
          >
            Sign in
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-gray-500">
          회원이 아니신가요?
          <RouterLink
            :to="{ name: 'signup' }"
            class="font-semibold text-indigo-600 hover:text-indigo-500"
          >
            회원가입
          </RouterLink>
        </p>
      </div>

    </div>

</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts';
import { useRouter } from 'vue-router';

const router = useRouter()

const username = ref(null)
const password = ref(null)

const accountStore = useAccountStore()

const login = async () => {
  const payload = {
    username: username.value,
    password: password.value,
  }

  try {
    await accountStore.logIn(payload)
    console.log(payload)
    router.push({ name: 'start' })   // ✅ 화면 제어는 여기서
  } catch (err) {
    console.log('login error status:', err.response?.status)
    console.log('login error data:', err.response?.data)
  }
}

const close = () => {
  router.push({ name: 'start' })
}

</script>

<style scoped>

</style>

