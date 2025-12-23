<template>
  <div class="nav-panel">
    <nav
      class="h-16 w-full pixel-panel__content flex"
    >
      <RouterLink :to="{ name: 'map'}" class="flex items-center justify-center flex-1">
        🗺️메인
      </RouterLink>

      <RouterLink :to="{ name: 'usermode'}" class="flex items-center justify-center flex-1">
        👤유저
      </RouterLink>

      <RouterLink :to="{ name: 'profile'}" class="flex items-center justify-center flex-1">
        ⭐홈
      </RouterLink>

      <RouterLink :to="{ name: 'aimode'}" class="flex items-center justify-center flex-1">
        🤖AI
      </RouterLink>
      <RouterLink :to="{ name: 'ranking'}" class="flex items-center justify-center flex-1">
        🤖랭킹
      </RouterLink>
    </nav>
</div>
</template>

<script setup>


</script>

<style scoped>

</style>