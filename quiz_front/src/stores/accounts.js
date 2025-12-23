import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {

  const API_URL = import.meta.env.VITE_AUTH_API_URL
//   const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)

  const user = ref(null)

  const router = useRouter()

  const signUp = async (payload) => {
    try {
      const res = await axios.post(
        `${API_URL}/accounts/signup/`,
        payload
      )
      return res

    } catch (err) {
      throw err
    }
  }

  const fetchMe = async () => {
    if (!token.value) return null
    const res = await axios.get(`${API_URL}/accounts/user/`, {
      headers: { Authorization: `Token ${token.value}` },
    })
    user.value = res.data
    return res.data
  }

  const logIn = async (payload) => {
    try {
      const res = await axios.post(`${API_URL}/accounts/login/`, payload)

      token.value = res.data.key

      await fetchMe()

      return res
    } catch (err) {
      throw err
    }
  }

  const isLogin = computed(() => {
    return token.value ? true : false
  })

  const userId = computed(() => user.value?.pk ?? null)

  const logOut = () => {
    token.value = null
    router.push({ name: 'start' })
  }

  return { token, user, userId, signUp, logIn, logOut, isLogin }
}, { persist: true }) 
