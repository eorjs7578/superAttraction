<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <img src="/images/logo.png" alt="logo" class="logo" />
          Super 이끌림
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'home' }">HOME</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'DepositProducts' }">예금 & 적금 금리 비교</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'ExchangeRatioCalc' }">환율 계산기</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'banksfind' }">지점 찾기</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'recommend' }">나에게 맞는 상품 추천</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'Article' }">커뮤니티</RouterLink>
            </li>
            <li v-if="!isLogin" class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'login' }">로그인</RouterLink>
            </li>
            <li v-if="!isLogin" class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'signup' }">회원가입</RouterLink>
            </li>
            <li v-if="isLogin" class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'ProfilePage' }">마이프로필</RouterLink>
            </li>
            <li v-if="isLogin" class="nav-item">
              <RouterLink class="nav-link" @click="logOut" :to="{ name: 'home' }">로그아웃</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import { computed, ref } from 'vue'

const counterStore = useCounterStore()
const router = useRouter()

const isLogin = computed(() => counterStore.isLogin)

const logOut = () => {
  counterStore.token = null
  console.log(counterStore.token)
  localStorage.removeItem('token')
  console.log('로그아웃 완료')
  counterStore.LogOut() // 스토어의 로그아웃 액션을 호출합니다. 이 부분은 스토어에 따라 달라질 수 있습니다.
  router.push({ name: 'home' }) // 홈 페이지로 리디렉션 합니다.
  sessionStorage.clear()
}
</script>

<style scoped>
/* Navbar */
.navbar {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.navbar:hover {
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.navbar-brand {
  font-size: 24px;
  font-weight: bold;
  color: #379cb6;
  margin-left: 10px;
  display: flex;
  align-items: center;
}

.navbar-brand .logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.navbar-nav .nav-item {
  margin-right: 20px;
}

.nav-link {
  color: #379cb6;
  font-size: 18px;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #0056b3;
}

.navbar-toggler {
  border: none;
}

.navbar-toggler-icon {
  background-color: #379cb6;
}

.navbar-nav.ms-auto .nav-item:last-child .nav-link {
  margin-right: 0;
}

/* Body */
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f8f9fa;
}
</style>
