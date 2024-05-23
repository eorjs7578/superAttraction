<template>
  <div>
    <h5>{{ article.id }}번째 글</h5>
    <p>제목 : {{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
    <RouterLink 
      :to="{ name: 'ArticleDetail', params: { id: article.id }}"
    >
      [DETAIL]
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  article: Object
})
</script>
