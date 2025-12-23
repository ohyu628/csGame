<template>
  <div>받은 id: {{ props.id }}</div>
</template>

<script setup>
const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
})
</script>

