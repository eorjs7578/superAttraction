<template>
  <div>
    <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel" data-bs-interval="2000">
      <div class="carousel-inner">
        <div v-for="(item, index) in images" :key="index" :class="{ 'carousel-item': true, 'active': index === 0 }">
          <!-- 이미지를 클릭하면 item.url로 이동 -->
          <a :href="item.url" target="_blank">
            <img :src="item.src" class="carousel-image" alt="Carousel Image">
          </a>
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
    
    <div class="news-section">
  <h2 class="recentnews">최신 뉴스</h2>
  <div class="news-list row row-cols-1 row-cols-md-4 g-4">
    <div class="col" v-for="article in newsArticles" :key="article.url">
      <div class="card h-100 news-item">
        <img :src="article.urlToImage" class="card-img-top" alt="News Image">
        <div class="card-body">
          <h5 class="card-title">{{ article.title }}</h5>
          <p class="card-text">{{ article.description }}</p>
        </div>
        <div class="card-footer">
          <a :href="article.url" target="_blank" class="btn btn-primary" style="background-color: #379cb6">자세히 보기</a>
        </div>
      </div>
    </div>
  </div>
</div>


    <!-- 부트스트랩 카드로 서비스 특징 소개 -->
    <div class="container">
      <br><h1 class="ourservice">우리의 서비스는</h1>
      <div class="row">
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">간편한 접근성</h5>
              <p class="card-text">우리 서비스는 사용하기 편리하고 직관적인 인터페이스를 제공하여 모든 사용자가 쉽게 접근할 수 있습니다.</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">다양한 기능</h5>
              <p class="card-text">다양한 기능과 옵션을 제공하여 사용자들이 자신에게 맞는 방식으로 서비스를 이용할 수 있습니다.</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">신속한 처리</h5>
              <p class="card-text">빠르고 효율적인 처리 과정을 통해 사용자들의 요구를 신속하게 처리하여 최상의 서비스 품질을 제공합니다.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const images = ref([]);
const newsArticles = ref([]);




const imageItems = [
  { src: "/images/image1.png", url: "https://www.kbstar.com/" },
  { src: "/images/image2.png", url: "https://www.ibk.co.kr/" },
  { src: "/images/image3.png", url: "https://www.nhbank.com/nhmn/KO_NHMN_01.do" },
  { src: "/images/image4.png", url: "https://www.shinhan.com/index.jsp" },
  { src: "/images/image5.png", url: "https://www.wooribank.com/" },
];

function setImages() {
  images.value = imageItems;
}

function fetchNews() {
  
  const url = `https://newsapi.org/v2/everything?q=은행&sortBy=popularity&apiKey=${import.meta.env.VITE_NEWS_API_KEY}`;
  axios.get(url)
    .then(response => {
      console.log(response.data);
      newsArticles.value = response.data.articles.slice(0, 8); // q=은행 이라 돼 있어서 동작 안 함
    })
    .catch(error => {
      console.error('Error fetching news:', error);
      alert('뉴스를 불러오는 데 실패했습니다. 콘솔을 확인하세요.');
    });
}


onMounted(() => {
  setImages();
  fetchNews();
  const myCarouselElement = document.querySelector('#carouselExampleAutoplaying');
  // Bootstrap Carousel initialization
  const carouselInstance = new bootstrap.Carousel(myCarouselElement, {
    interval: 2000,
    ride: 'carousel'
  });


  // Cleanup on unmount
  onUnmounted(() => {
    carouselInstance.dispose();
  });
});
</script>

<style scoped>
body {
  font-family: 'Roboto', sans-serif;
}
.card {
  border: none; /* 카드 테두리 제거 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 카드 그림자 추가 */
}

.card-body {
  padding: 20px; /* 카드 내부 여백 조절 */
}

.card-title {
  font-weight: bold; /* 카드 제목의 폰트 굵기를 높임 */
}

.card-text {
  color: #555; /* 카드 텍스트 컬러를 어두운 회색으로 설정 */
}

/* 캐러셀 스타일 */
.carousel-inner {
  text-align: center;
  padding: 5%;
  background-color: #fff;
  border-radius: 15px;
  margin-top: 20px;
}

.carousel-control-prev,
.carousel-control-next {
  top: 50%;
  transform: translateY(-50%);
}

.carousel-control-prev {
  left: 0;
}

.carousel-control-next {
  right: 0;
}

.carousel-image {
  max-height: 300px;
  max-width: 100%;
  object-fit: contain;
}

.recentnews{
  padding-top: 15px;
  color: #379cb6;
  font-weight: bold;
}

.news-section h2 {
  text-align: center;
  margin-bottom: 20px;
}

.news-section ul {
  list-style-type: none;
  padding: 0;
}

.news-section li {
  margin-bottom: 20px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 20px;
}


</style>