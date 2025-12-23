<template>

<div class="relative justify-center w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
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
          Create your account
        </h2>
      </div>

      <!-- 로그인 폼 -->
      <div class="mt-8">
        <form @submit.prevent="signUp" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-900">
              Username
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
            <label for="username" class="block text-sm font-medium text-gray-900">
              Email
            </label>
            <div class="mt-2">
              <input
                v-model.trim="email"
                id="email"
                type="email"
                autocomplete="current-email"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>
          <div>
            <label for="password1" class="block text-sm font-medium text-gray-900">
              Password
            </label>
            <div class="mt-2">
              <input
                v-model.trim="password1"
                id="password1"
                type="password"
                autocomplete="new-password"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>
          <div>
            <label for="password2" class="block text-sm font-medium text-gray-900">
              Password
            </label>
            <div class="mt-2">
              <input
                v-model.trim="password2"
                id="password2"
                type="password"
                autocomplete="new-password"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          <button
            type="submit"
            class="w-full rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
          >
            Sign Up
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-gray-500">
          이미 계정이 있습니다
          <RouterLink
            :to="{ name: 'login' }"
            class="font-semibold text-indigo-600 hover:text-indigo-500"
          >
            로그인
          </RouterLink>
        </p>
      </div>

    </div>

</template>

<script setup>
  import { ref } from 'vue'
  import { useAccountStore } from '@/stores/accounts'
  import { useRouter } from 'vue-router'

  const router = useRouter()

  const email = ref(null)
  const username = ref(null)
  const password1 = ref(null)
  const password2 = ref(null)
  

  const accountStore = useAccountStore()


const signUp = async () => {
  console.log("회원가입 요청 전송")
  const payload = {
    email: email.value,
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  }

  try {
    await accountStore.signUp(payload)
    console.log(payload)
    
    await accountStore.logIn({
      username: payload.username,
      password: payload.password1,
    })

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