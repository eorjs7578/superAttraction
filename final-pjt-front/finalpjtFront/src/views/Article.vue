<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header bg-custom text-white text-center">
            <h1 class="card-title">게시판</h1>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-end mb-3">
              <RouterLink :to="{ name: 'ArticleCreate' }" class="btn btn-custom">
                [CREATE]
              </RouterLink>
            </div>
            <ArticleList />
            <div class="text-center mt-4">
              <button @click="goHome" class="btn btn-secondary">Home으로</button>
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
import { RouterLink, useRouter } from 'vue-router';
import ArticleList from '@/components/ArticleList.vue';

const router = useRouter();
const store = useCounterStore();

onMounted(() => {
  store.getArticles();
});

const goHome = () => {
  router.push({ name: 'home' });
};
</script>

<style scoped>
.container {
  max-width: 1400px;
}

.card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  background-color: #fff; /* 카드 배경색 설정 */
}

.card-header {
  border-radius: 8px 8px 0 0;
  background-color: #379cb6; /* 헤더 배경색 설정 */
}

.card-title {
  font-family: 'Arial', sans-serif;
  color: #fff;
}

.card-body {
  color: #333;
}

.btn-custom {
  background-color: #379cb6; /* CREATE 버튼 배경색 설정 */
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

.text-white {
  color: #fff;
}
</style>
