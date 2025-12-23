<template>
  <div class="h-screen flex flex-col bg-gray-500 text-white relative min-h-0">
    <div class="flex-1 overflow-hidden flex flex-col min-h-0">
      <!-- ✅ 상단 유저 정보 바 -->
      <div class="nav-panel">
        <div class="pixel-panel__content flex items-center justify-between">
          <div>
            <span class="bg-black">뱃지</span>
            <span>| {{ username }} |</span>
            <span>Lv: {{ level }} |</span>
            <span>Exp: {{ exp }} |</span>
          </div>

          <!-- ✅ 오른쪽 끝 메뉴 버튼 -->
          <button
            class="px-3 py-1 border rounded bg-white/10 hover:bg-white/20"
            @click="openMenu"
          >
            ☰
          </button>
        </div>
      </div>

      <!-- ✅ 여기 RouterView 영역에 전환 적용 -->
      <div class="flex flex-1 relative overflow-hidden p-2 min-h-0">
        <RouterView v-slot="{ Component, route }">
          <component :is="Component" :key="route.fullPath" />
        </RouterView>

        <Transition name="route-dim">
          <div v-if="isTransitioning" class="absolute inset-0 bg-black z-50 pointer-events-none" />
        </Transition>
      </div>
    </div>

    <NavBar />

    <!-- ✅ 메뉴 모달 (로컬 state로만 제어) -->
    <BaseModal v-if="isMenuOpen" @close="closeMenu">
      <LogoutConfirmModal
        @close="closeMenu"
        @logout="onLogout"
      />
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAccountStore } from '@/stores/accounts'

import NavBar from '@/components/NavBar.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import LogoutConfirmModal from '@/components/LogoutConfirmModal.vue'

const userStore = useUserStore()
const accountStore = useAccountStore()
const router = useRouter()

const username = userStore.username
const level = userStore.level
const exp = userStore.exp

// ✅ 전역 modal store 대신 로컬 state 사용
const isMenuOpen = ref(false)

// ✅ 라우트 전환 오버레이 상태
const isTransitioning = ref(false)

// ✅ 라우터 가드 등록/해제용
let removeBefore = null
let removeAfter = null

onMounted(() => {
  userStore.fetchUser()

  // 이동 시작 -> 즉시 어둡게
  removeBefore = router.beforeEach((to, from, next) => {
    isTransitioning.value = true
    next()
  })

  // 이동 완료 -> 서서히 밝아지게(오버레이 제거)
  removeAfter = router.afterEach(() => {
    setTimeout(() => {
      isTransitioning.value = false
    }, 50)
  })
})

onBeforeUnmount(() => {
  // ✅ 중복 등록 방지(중요)
  if (removeBefore) removeBefore()
  if (removeAfter) removeAfter()
})

const openMenu = () => {
  isMenuOpen.value = true
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const onLogout = () => {
  accountStore.logOut()
  closeMenu()
}
</script>

<style scoped>
/* ✅ 오버레이 트랜지션: 깔릴 때는 즉시, 사라질 때만 부드럽게 */
.route-dim-enter-from,
.route-dim-leave-to {
  opacity: 0.2;
}

.route-dim-enter-to,
.route-dim-leave-from {
  opacity: 1;
}

/* 들어올 땐 즉시 깔림 */
.route-dim-enter-active {
  transition: opacity 0ms;
}

/* 나갈 땐 서서히 사라지면서 "밝아짐" 느낌 */
.route-dim-leave-active {
  transition: opacity 800ms ease-out;
}
</style>

