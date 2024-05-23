<template>
  <div>
    <h1>프로필 수정 페이지</h1>
    <hr>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="nickname">닉네임:</label>
        <input type="text" id="nickname" v-model="updatedProfile.nickname" required>
      </div>
      <div>
        <label for="age">나이:</label>
        <input type="number" id="age" v-model="updatedProfile.age" required>
      </div>
      <div>
        <label for="gender">성별:</label>
        <select id="gender" v-model="updatedProfile.gender">
          <option v-for="option in genderOptions" :key="option.value" :value="option.value">
            {{ option.text }}
          </option>
        </select>
      </div>
      <div>
        <label for="salary">연봉:</label>
        <select v-model="updatedProfile.salary" id="salary">
          <option v-for="option in salaryOptions" :key="option.value" :value="option.value">
            {{ option.text }}
          </option>
        </select>
      </div>
      <button type="submit">저장</button>
    </form>
    <button @click="goBack">취소</button>
  </div>
</template>

<script setup>
const genderOptions = [
  { value: '남성', text: '남성' },
  { value: '여성', text: '여성' },
]

const salaryOptions = [
  { value: '0~3000만원 미만', text: '0~3000만원 미만' },
  { value: '3000~6000만원 미만', text: '3000~6000만원 미만' },
  { value: '6000~1억미만', text: '6000~1억미만' },
  { value: '1억 이상', text: '1억 이상' }
]

import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const store = useCounterStore();
const router = useRouter();

// 저장된 프로필 데이터를 복사하여 수정에 사용
const updatedProfile = ref({
  nickname: '',
  age: '',
  gender: '',
  salary: ''
});

// 컴포넌트가 마운트될 때 현재 프로필 정보를 가져옵니다.
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/user/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
  .then((response) => {
    const profile = response.data;
    updatedProfile.value.nickname = profile.nickname;
    updatedProfile.value.age = profile.age;
    updatedProfile.value.gender = profile.gender;
    updatedProfile.value.salary = profile.salary;
  })
  .catch((error) => {
    console.error('프로필 정보를 불러오는 중 오류가 발생했습니다.', error);
  });
});

const updateProfile = () => {
  axios({
    method: 'put',
    url: `http://127.0.0.1:8000/user/edit/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: updatedProfile.value
  })
  .then(() => {
    store.getProfile()
    alert('프로필이 성공적으로 수정되었습니다.');
    router.push({ name: 'ProfilePage' });
  })
  .catch((error) => {
    console.error('프로필 수정 중 오류가 발생했습니다.', error);
  });
}

const goBack = () => {
  router.push({ name: 'ProfilePage' })
}
</script>

<style scoped>
/* 스타일을 여기에 추가하세요 */
form {
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 10px;
}

label {
  margin-right: 10px;
}

input, select {
  padding: 5px;
  font-size: 16px;
}

button {
  margin-top: 10px;
  padding: 10px;
  font-size: 16px;
}
</style>
