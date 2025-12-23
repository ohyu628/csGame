import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useUserStore } from '@/stores/user'

import StartPage from '@/views/StartPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import SignUpPage from '@/components/SignUpPage.vue'
import MainPage from '@/views/MainPage.vue'

import Map from '@/views/Map.vue'
import Stage from '@/views/Stage.vue'
import GameView from '@/views/GameView.vue'
import UserMode from '@/views/UserMode.vue'
import Profile from '@/views/Profile.vue'
import MyProblemSet from '@/views/MyProblemSet.vue'
import AIMode from '@/views/AIMode.vue'
import Ranking from '@/views/Ranking.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
  {
    path: '/',
    name: 'start',
    component: StartPage,
    children: [
        { path: 'login', name: 'login', component: LoginPage },
        { path: 'signup', name: 'signup', component: SignUpPage },
    ]

  },
  {
    path: '/main',
    name: 'main',
    component: MainPage,
    children: [
      { path: 'map', name: 'map', component: Map },
      { path: 'map/:mapid', name: 'stage', component: Stage},
      { path: 'game/:id', name: 'game', component: GameView},
      { path: 'usermode', name: 'usermode', component: UserMode},
      { path: 'profile', name: 'profile', component: Profile},
      { path: 'profile/problemset', name: 'myproblemset', component: MyProblemSet},
      { path: 'ai', name: 'aimode', component: AIMode},
      { path: 'ranking', name: 'ranking', component: Ranking},
    ]
  },

  ],
})


router.beforeEach(async (to, from) => {
  const accountStore = useAccountStore()
  const userStore = useUserStore()

  if (to.name === 'main' && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'login' }
  }

  if ((to.name === 'signup' || to.name === 'login') && (accountStore.isLogin) ) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'start' }
  }

  if (accountStore.isLogin && !userStore.loaded) {
      try {
        await userStore.fetchUser()
        
      } catch (err) {
        // 토큰 만료 / 인증 실패
        accountStore.logOut?.()
        return { name: 'login' }
      }
    }

})

export default router
