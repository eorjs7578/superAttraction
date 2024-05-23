<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <form @submit.prevent="signUp" class="signup-form">
      <div class="form-section">
        <h3>기본정보</h3>
        <div class="form-group">
          <label for="username">ID : </label>
          <input type="text" v-model.trim="username" id="username" required>
        </div>
        <div class="form-group">
          <label for="password1">비밀번호 : </label>
          <input type="password" v-model.trim="password1" id="password1" required>
        </div>
        <div class="form-group">
          <label for="password2">비밀번호 확인 : </label>
          <input type="password" v-model.trim="password2" id="password2" required>
          <span v-if="password1 !== password2" class="error">비밀번호가 다릅니다</span>
        </div>
      </div>
      <hr>
      <div class="form-section">
        <h3>상세정보</h3>
        <div class="form-group">
          <label for="nickname">닉네임 : </label>
          <input type="text" v-model.trim="nickname" id="nickname" required>
        </div>
        <div class="form-group">
          <label for="age">나이 : </label>
          <input type="text" v-model="age" id="age" required>
        </div>
        <div class="form-group">
          <label for="gender">성별 : </label>
          <select v-model="gender" id="gender" class="form-select" required>
            <option v-for="option in genderOptions" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="salary">연봉 : </label>
          <select v-model="salary" id="salary" class="form-select" required>
            <option v-for="option in salaryOptions" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>
      </div>
      <button type="submit" class="submit-btn">가입하기</button>
    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)
const age = ref('')
const gender = ref('')
const salary = ref('')
const store = useCounterStore()

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

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    age: age.value,
    gender: gender.value,
    salary: salary.value,
  }
  store.signUp(payload)
}

</script>

<style>
.signup-container {
  width: 80%; /* 수정: 적당한 너비로 조정 */
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  background-color: #fff; /* 배경색 추가 */
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.form-section {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control, .form-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.submit-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #0056b3;
}

hr {
  margin-top: 20px;
  margin-bottom: 20px;
}

.error {
  color: #ff6b6b; /* Bright color for error messages */
  font-size: 0.9em; /* Smaller font size for errors */
}


</style>
