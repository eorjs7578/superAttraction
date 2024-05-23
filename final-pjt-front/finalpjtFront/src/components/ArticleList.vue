<template>
  <div class="article-list-container">
    <h3>글 목록</h3>
    <div v-if="store.articles.length > 0">
      <ArticleListItem 
        v-for="article in store.articles"
        :key="article.id"
        :article="article"
      />
    </div>
    <div v-else>
      <p>게시물이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import ArticleListItem from '@/components/ArticleListItem.vue'

const store = useCounterStore()
</script>

<style scoped>
/* 게시글 목록 컨테이너 */
.article-list-container {
  max-width: 800px; /* 최대 너비 설정 */
  margin: auto; /* 가운데 정렬 */
  padding: 20px;
  font-family: 'Roboto', sans-serif; /* Roboto 폰트 사용 */
}

/* 글 목록 제목 */
.article-list-container h3 {
  margin-bottom: 20px; /* 제목 아래 여백 설정 */
}

/* 게시물이 없는 경우 안내 문구 */
.article-list-container p {
  color: #555; /* 텍스트 컬러 설정 */
}
</style>
