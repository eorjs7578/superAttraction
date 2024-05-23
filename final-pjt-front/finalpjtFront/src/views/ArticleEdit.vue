<template>
  <div class="edit-page-container">
    <h1>글 수정</h1>
    <form @submit.prevent="submitForm" class="edit-form">
      <div class="form-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model="formData.title" required>
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea id="content" v-model="formData.content" required></textarea>
      </div>
      <button type="submit">수정하기</button>
    </form>
    <button @click="goBack" class="back-button">뒤로가기</button>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter'

const formData = ref({
  title: '',
  content: '',
});

const store = useCounterStore()
const router = useRouter();
const route = useRoute();
const articleId = route.params.id;

const goBack = () => {
  router.back();
}

// 글 수정 페이지 로드 시, 현재 글 내용 불러오기
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${articleId}/`
  })
    .then((response) => {
      const article = response.data;
      formData.value.title = article.title;
      formData.value.content = article.content;
    })
    .catch((error) => {
      console.error('글 정보를 불러오는 중 오류가 발생했습니다.', error);
    });
});

// 폼 제출 시 글 수정 요청
const submitForm = () => {
  axios({
    method: 'put',
    url: `${store.API_URL}/api/v1/articles/${articleId}/Edit`,
    data: {
      title: formData.value.title,
      content: formData.value.content
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(() => {
      store.getArticles()
      alert('글이 성공적으로 수정되었습니다.');
      router.push({ name: 'ArticleDetail', params: { id: articleId } });
    })
    .catch((error) => {
      console.error('글 수정 중 오류가 발생했습니다.', error);
    });
}
</script>

<style scoped>
.edit-page-container {
  max-width: 600px; /* 최대 너비 설정 */
  margin: 50px auto; /* 상단 여백을 50px로 설정하고 좌우는 자동으로 설정하여 가운데 정렬합니다. */
  padding: 20px; /* 안쪽 여백 설정 */
  border: 1px solid #ccc; /* 테두리 추가 */
  border-radius: 8px; /* 모서리를 둥글게 설정 */
}

.edit-form .form-group {
  margin-bottom: 20px; /* 각 입력 요소 사이의 간격 설정 */
}

.edit-form label {
  font-weight: bold; /* 제목 굵게 설정 */
  display: block; /* 블록 요소로 설정하여 줄 바꿈 추가 */
}

.edit-form .form-control {
  width: calc(100% - 22px); /* 입력 요소의 너비를 100%로 설정하되, 패딩과 테두리의 크기를 고려하여 조정 */
  padding: 10px; /* 안쪽 여백 설정 */
  border: 1px solid #ccc; /* 테두리 추가 */
  border-radius: 4px; /* 모서리를 둥글게 설정 */
}
.edit-form textarea {
  width: calc(105% - 22px); /* 텍스트 영역의 너비를 100%로 설정하되, 패딩과 테두리의 크기를 고려하여 조정 */
  height: 300px; /* 높이를 200px로 설정하여 크기를 키웁니다. */
  padding: 10px; /* 안쪽 여백 설정 */
  border: 1px solid #ccc; /* 테두리 추가 */
  border-radius: 4px; /* 모서리를 둥글게 설정 */
}


.edit-form button {
  background-color: #007bff; /* 배경색 설정 */
  color: white; /* 글자색 설정 */
  padding: 10px 20px; /* 안쪽 여백 설정 */
  border: none; /* 테두리 없앰 */
  border-radius: 4px; /* 모서리를 둥글게 설정 */
  cursor: pointer; /* 커서를 포인터로 변경하여 클릭 가능한 상태로 표시 */
  font-size: 16px; /* 글자 크기 설정 */
  transition: background-color 0.2s; /* 배경색 변화에 트랜지션 효과 추가 */
}

.edit-form button:hover {
  background-color: #0056b3; /* 마우스를 올렸을 때 배경색 변경 */
}

.back-button {
  background-color: #f9f9f9; /* 배경색 설정 */
  border: 1px solid #ddd; /* 테두리 추가 */
  padding: 10px 20px; /* 안쪽 여백 설정 */
  border-radius: 4px; /* 모서리를 둥글게 설정 */
  cursor: pointer; /* 커서를 포인터로 변경하여 클릭 가능한 상태로 표시 */
  font-size: 16px; /* 글자 크기 설정 */
  margin-top: 20px; /* 위쪽 여백 설정 */
}

.back-button:hover {
  background-color: #e9e9e9; /* 마우스를 올렸을 때 배경색 변경 */
}

</style>

  