<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-custom text-white text-center">
            <h1 class="card-title">{{ profile.username }}님의 프로필 페이지입니다.</h1>
          </div>
          <div class="card-body text-center">
            <h2 class="text-secondary">상세정보</h2>
            <br>
            <p><strong>닉네임:</strong> {{ profile.nickname }}</p>
            <p><strong>나이:</strong> {{ profile.age }}세</p>
            <p><strong>성별:</strong> {{ profile.gender }}</p>
            <p><strong>연봉:</strong> {{ profile.salary }}</p>
            <hr>
            <ProfileProducts />
            <hr>
            <div class="d-flex justify-content-around">
              <button class="btn btn-custom" @click="editProfile">프로필 수정</button>
              <button class="btn btn-danger" @click="deleteProfile">회원탈퇴</button>
            </div>
            <br>
            <div class="text-center">
              <button class="btn btn-secondary" @click="goHome">Home으로</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';
import ProfileProducts from '@/components/ProfileProducts.vue';

const store = useCounterStore();
const router = useRouter();

onMounted(() => {
  store.getProfile();
});

const profile = store.profile;

const editProfile = () => {
  router.push({ name: 'ProfileEdit' });
};

const deleteProfile = () => {
  store.deleteProfile();
};

const goHome = () => {
  router.push({ name: 'home' });
};
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
}

.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  background-color: #fff;
}

.card-header {
  border-radius: 8px 8px 0 0;
  background-color: #379cb6;
}

.card-title {
  font-family: 'Arial', sans-serif;
  color: #fff;
}

.card-body {
  color: #333;
  text-align: center; /* 본문 텍스트 중앙 정렬 */
}

h2 {
  font-family: 'Arial', sans-serif;
  color: #333;
}

p {
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #666;
}

.btn-custom {
  background-color: #379cb6;
  color: white;
  font-weight: bold;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  text-decoration: none;
}

.btn-custom:hover {
  background-color: darken(#379cb6, 10%);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-secondary:hover {
  background-color: darken(#6c757d, 10%);
}

.text-secondary {
  color: #6c757d !important;
}

hr {
  border-top: 1px solid #eee;
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
