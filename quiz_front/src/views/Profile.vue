<template>
  <div class="h-full w-full min-h-0 text-black flex flex-col">
    <!-- ✅ 전체를 감싸는 패널은 딱 1개 -->
    <div class="flex-1 min-h-0">
      <div class=" flex flex-col h-full min-h-0 gap-2">

        <!-- ✅ 위/아래 1:1 분할 -->
        <div class="flex-1 min-h-0 grid grid-cols-2 gap-2">
          <!-- ✅ 위쪽 왼쪽: 스프라이트 (패널 X) -->
          <div class="relative min-h-0 overflow-hidden flex items-center justify-center bg-black/5 rounded">
            <SpriteSheet
              :src="idleSheet"
              :frameWidth="128"
              :frameHeight="128"
              :frames="8"
              :fps="8"
              :scale="2"
              class="[image-rendering:pixelated]"
            />
          </div>

          <!-- ✅ 위쪽 오른쪽: 스테이터스 (패널 X) -->
            <Status />

        </div>

        <!-- ✅ 아래쪽 1/2 영역 -->
        <div class="flex-1 min-h-0 flex flex-col justify-center items-center gap-2 bg-black/5 rounded p-2">
          <RouterLink :to="{ name: 'myproblemset' }" class="underline">
            내 문제 관리
          </RouterLink>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import idleSheet from "@/assets/character/Test_animation-Sheet.png";
import SpriteSheet from "@/components/SpriteSheet.vue";
import Status from "@/components/Status.vue"
import { useAccountStore } from "@/stores/accounts"

const accountStore = useAccountStore()

onMounted(async () => {
  // ✅ 로그인한 상태인데 user가 비어있으면 서버에서 가져오기
  if (!accountStore.user) {
    await accountStore.fetchMe?.() // 너 스토어 함수명이 fetchMe가 아니면 그걸로 변경
  }
})
</script>

<style scoped>

</style>