<template>
  <div class="article-details">
    <h1>글 세부정보</h1>
    <div v-if="article" class="article-info">
      <p>{{ article.id }}번째 글</p>
      <hr>
      <p v-if="article.user === currentUserPk">{{ store.profile.username }}님의 글</p> 
      <p class="article-title">제목 : {{ article.title }}</p>
      <p class="article-content">내용 : {{ article.content }}</p>
      <div class="article-meta">
        <p>작성일 : {{ article.created_at }}</p>
        <p>수정일 : {{ article.updated_at }}</p>
      </div>

      <!-- 수정 및 삭제 버튼이 현재 사용자가 글의 작성자인 경우에만 보이도록 함 -->
      <div v-if="article.user === currentUserPk" class="action-buttons">
        <button @click="editArticle">수정</button>
        <button @click="deleteArticle">삭제</button>
      </div>
    </div>
    <button @click="goBack" class="back-button">뒤로가기</button>
  </div>
</template>


<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute, useRouter } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)

// 현재 사용자의 pk를 가져옵니다. 이 예제에서는 useCounterStore에서 관리한다고 가정합니다.
const currentUserPk = store.profile.pk
console.log(`작성자pk값 : ${store.profile.pk}`)

const goBack = () => {
  router.push({ name: 'Article' })
}

const editArticle = () => {
  router.push({ name: 'ArticleEdit', params: { id: article.value.id } })
}

const deleteArticle = () => {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/delete`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(() => {
      store.getArticles()
      alert('글이 삭제되었습니다.');
      // Article 목록 페이지로 리다이렉트
      router.push({ name: 'Article' });
    })
    .catch((error) => {
      console.log(error);
    });
};


onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`
  })
    .then((response) => {
      article.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
})
</script>


<style scoped>
.article-details {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.article-info {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.article-title {
  font-size: 24px;
  font-weight: bold;
}

.article-content {
  margin-top: 10px;
  font-size: 18px;
}

.article-meta {
  margin-top: 20px;
}

.action-buttons button {
  margin-right: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 16px;
}

.action-buttons button:hover {
  background-color: #0056b3;
}

.back-button {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.back-button:hover {
  background-color: #e9e9e9;
}
</style>
