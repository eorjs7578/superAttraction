<template>
  <div class="login">
    <img src="/images/attraction_logo.png" alt="이끌림">
    
    <form @submit.prevent="logIn">
      <div>
        <label for="username">ID : </label>
        <input type="text" v-model.trim="username" id="username" required>
      </div>
      <div>
        <label for="password">비밀번호 : </label>
        <input type="password" v-model.trim="password" id="password" required>
      </div>
      <input type="submit" value="로그인">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null)
const password = ref(null)
const store = useCounterStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

</script>

<style>
.login {
  border: 1px solid rgba(0, 0, 0, 0.2);
  width: 400px;
  margin: auto;
  height: auto; /* Adjusted for content */
  color: #0e0d0d; /* Changed for better contrast */
  border-radius: 20px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.75);
  padding: 40px; /* Added padding around the content */
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 20px; /* Increased gap for better spacing */
}

input[type="text"],
input[type="password"] {
  width: 100%; /* Full width */
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc; /* Subtle border */
  background-color: rgba(255, 255, 255, 0.8); /* Light background for readability */
}

input[type="submit"] {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
  background-color: #0056b3;
}

h1 {
  margin-bottom: 20px; /* More space above the form */
  text-align: center;
  font-weight: bold;
  font-size: 24px; /* Larger font size for emphasis */
}

.error {
  color: #ff6b6b; /* Bright color for error messages */
  font-size: 0.9em; /* Smaller font size for errors */
}

</style>
