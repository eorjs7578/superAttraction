import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ExchangeRatioCalc from '@/views/ExchangeRatioCalc.vue'

import BankFind from '@/views/BankFind.vue'
import DepositProducts from '@/views/DepositProducts.vue'
import DepositProductDetail  from '@/views/DepositProductDetail.vue'
import installmentSavingProducts from '@/views/installmentSavingProducts.vue'

import Login from '@/views/Login.vue'
import SignUp from '@/views/SignUp.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import ProfileEdit from '@/views/ProfileEdit.vue'

import Article from '@/views/Article.vue'
import ArticleDetail from '@/views/ArticleDetail.vue'
import ArticleCreate from '@/views/ArticleCreate.vue'
import ArticleEdit from '@/views/ArticleEdit.vue' // 수정 페이지 컴포넌트

import Recommend from '@/views/Recommend.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/exchange-ratio-calc',
      name: 'ExchangeRatioCalc',
      component: ExchangeRatioCalc
    },
    {
      path: '/installment-Saving-Products',
      name: 'installmentSavingProducts',
      component: installmentSavingProducts
    },
    {
      path: '/banks-find',
      name: 'banksfind',
      component: BankFind
    },
    {
      path: '/Deposit-Products',
      name: 'DepositProducts',
      component: DepositProducts
    },
    {
      path: '/:productId',
      name: 'DepositProductDetail',
      component: DepositProductDetail
    },
    {
      path: '/Login',
      name: 'login',
      component: Login
    },
    {
      path: '/SignUp',
      name: 'signup',
      component: SignUp
    },
    {
      path: '/profilePage',
      name: 'ProfilePage',
      component: ProfilePage
    },
    {
      path: '/ProfileEdit',
      name: 'ProfileEdit',
      component: ProfileEdit
    },
    {
      path: '/Article',
      name: 'Article',
      component: Article
    },
    {
      path: '/Articles/:id',
      name: 'ArticleDetail',
      component: ArticleDetail
    },
    {
      path: '/ArticleCreate',
      name: 'ArticleCreate',
      component: ArticleCreate
    },
    {
      path: '/Articles/:id/Edit',
      name: 'ArticleEdit', // 이 부분이 중요합니다.
      component: ArticleEdit
    },
    {
      path: '/Recommend',
      name: 'recommend',
      component: Recommend
    },
  ]
})

import { useCounterStore } from '@/stores/counter'


router.beforeEach((to, from) => {
  const store = useCounterStore()
  // 인증되지 않은 사용자는 메인 페이지에 접근 할 수 없음
  if (to.name === 'Article' && store.isLogin === false) {
    window.alert('로그인이 필요해요!!')
    return { name: 'Login' }
  }

  // 인증된 사용자는 회원가입과 로그인 페이지에 접근 할 수 없음
  if ((to.name === 'SignUpV' || to.name === 'Login') && (store.isLogin === true)) {
    window.alert('이미 로그인 했습니다.')
    return { name: 'ArticleView' }
  }
})

// router.beforeEach((to, from, next) => {
//   if (to.name === 'home') {
//     // 새로고침을 실행합니다.
//     window.location.reload()
//   } else {
//     next()
//   }
// })

export default router
