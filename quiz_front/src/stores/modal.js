import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalStore = defineStore('modal', () => {
  const isOpen = ref(false)
  const targetId = ref(null)

  const open = (id) => {
    targetId.value = id
    isOpen.value = true
  }

  const close = () => {
    isOpen.value = false
    targetId.value = null
  }

  return { isOpen, targetId, open, close }
})