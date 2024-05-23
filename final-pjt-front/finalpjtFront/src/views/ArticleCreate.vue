<template>
  <div class="article-creation">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle" class="article-form">
      <div class="form-group">
        <label for="title">제목 : </label>
        <input type="text" v-model.trim="title" id="title" class="form-control">
      </div>
      <div class="form-group">
        <label for="content">내용 : </label>
        <textarea v-model.trim="content" id="content" class="form-control"></textarea>
      </div>
      <button type="submit" class="submit-button">작성 완료</button>
    </form>
    <button @click="goBack" class="back-button">뒤로가기</button>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const title = ref(null)
const content = ref(null)
const router = useRouter()

const createArticle = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/`,
    data: {
      title: title.value,
      content: content.value
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((response) => {
      // console.log(response.data)
      store.getArticles()
      router.push({ name: 'Article' })
    })
    .catch((error) => {
      console.log(error)
    })
}

const goBack = () => {
  router.back()
}

</script>

<style scoped>
.article-creation {
  max-width: 600px;
  margin: 30px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.article-form .form-group {
  margin-bottom: 20px;
}

.article-form label {
  font-weight: bold;
  display: block;
}

.article-form .form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical; /* 세로 크기 조절 가능 */
  overflow-y: auto; /* 내용이 textarea 크기를 벗어나면 스크롤 생성 */
}

.submit-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.back-button {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

.back-button:hover {
  background-color: #e9e9e9;
}
</style>
