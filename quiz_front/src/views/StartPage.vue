<template>
  <!-- ✅ 최상단 컨테이너: 배경을 깔기 위해 min-h-screen + overflow-hidden 권장 -->
  <div class="relative min-h-screen overflow-hidden flex flex-col">

    <!-- ✅ 배경 레이어 (div) -->
    <div class="absolute inset-0 bg-start-bg bg-cover bg-center bg-no-repeat"></div>

    <!-- (선택) 배경 어둡게 덮는 오버레이 -->
    <div class="absolute inset-0 bg-black/30"></div>

    <!-- ✅ 실제 UI 레이어: 배경보다 위로 -->
    <div class="relative z-10 flex min-h-screen flex-col">
      <div class="min-h-screen flex items-center justify-center flex-col">
        <div class="fixed top-0 h-32 flex items-center justify-center">
          <h1>TITLE IMAGE</h1>
        </div>

        <!-- 로그인/회원가입 모달 -->
        <Transition name="modal">
          <div
            v-if="$route.name === 'login' || $route.name === 'signup'"
            class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          >
            <RouterView />
          </div>
        </Transition>
      </div>

      <!-- Press to Start -->
      <div
        v-if="showStartButton"
        @click="$router.push({ name: 'main' })"
        class="fixed inset-0 z-10 flex items-end justify-center pb-[25%] cursor-pointer"
      >
        <span class="text-lg font-semibold animate-fade-blink">
          Press to Start
        </span>
      </div>

      <!-- 로그인/회원가입 버튼 -->
      <div
        v-if="showMainButtons"
        class="absolute left-0 right-0 bottom-[20%] z-10 flex flex-col gap-4 px-6"
      >
        <RouterLink
          :to="{ name: 'login' }"
          class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500"
        >
          로그인
        </RouterLink>

        <RouterLink
          :to="{ name: 'signup' }"
          class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500"
        >
          회원가입
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
const route = useRoute()
const accountStore = useAccountStore()
const router = useRouter()
const showMainButtons = computed(() =>
  !['login', 'signup'].includes(route.name) &&
  !accountStore.isLogin
)

const showStartButton = computed(() =>
  accountStore.isLogin
  )


</script>

<style scoped>
.bg-start-bg {
  background-image: url("@/assets/background/start-bg.png");
}
</style>