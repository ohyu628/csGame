import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useUserStore = defineStore('user', {
  state: () => ({
    loaded: false,
    username: '',
    level: 1,
    exp: 0,
    maxExp: 100,
  }),

  getters: {
    expPercent(state) {
      return Math.min((state.exp / state.maxExp) * 100, 100)
    },
  },

  actions: {
    async fetchUser() {
      if (this.loaded) return
      

      const API_URL = import.meta.env.VITE_REST_API_URL
      const accountStore = useAccountStore()
      
      const res = await axios.get(`${API_URL}/profile/`, {
        headers: {
            Authorization: `Token ${accountStore.token}`
          }
        })

      const data = res.data

      this.username = data.username
      this.level = data.level
      this.exp = data.exp
      this.maxExp = data.max_exp
      this.loaded = true
    },

  clearUser() {
    this.$reset()
  },

    applySessionResult(result) {
    if (!result) return

    this.level = result.level_after
    this.exp = result.experience
    this.maxExp = this.level * 100
    this.loaded = true
    },
  },
})