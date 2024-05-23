<template>
  <div v-if="product" class="container my-4">
    <div class="card">
      <div class="card-body text-center">
        <div class="product-header">
          <img :src="bankLogos[product.kor_co_nm]" alt="Bank Logo" class="bank-logo">
        </div>
        <h2 class="card-title">{{ product.fin_prdt_nm }}</h2>
        
        <div class="section">
          <h3>{{ product.depositoptions_set[0].intr_rate_type_nm }}</h3>
          <div class="rate-box card text-center bg-light">
            <div class="card-body">
              <p><strong>{{ highestInterestOption.save_trm }}개월</strong></p>
              <p>최고: <strong>{{ highestInterestOption.intr_rate2 }}%</strong></p>
              <p>기본: {{ highestInterestOption.intr_rate }}% + 우대: {{ (highestInterestOption.intr_rate2 - highestInterestOption.intr_rate).toFixed(2) }}%</p>
              <!-- 계산하기 버튼 추가 -->
              <div class="mt-3 d-inline-block">
                <div class="input-group">
                  <input type="number" class="form-control form-control-lg" v-model="amount" placeholder="금액 입력">
                  <button class="btn btn-primary btn-lg" type="button" @click="calculate">계산</button>
                </div>
                <div v-if="calculatedValue !== null" class="mt-2">
                  <p>입금 금액: {{ amount }}원</p>
                  <p>{{ highestInterestOption.save_trm }}개월 후 예상 금액: {{ calculatedValue.toFixed(2) }}원</p>
                </div>
              </div>
            </div>
          </div>
        </div> 

        <div class="section">
          <h3>가입방법</h3>
          <p>{{ product.join_way }}</p>
        </div>

        <div class="section">
          <h3>가입대상</h3>
          <p>{{ product.join_member }}</p>
          <h3>개월별 금리</h3>
          <table class="table table-striped mx-auto">
            <thead>
              <tr>
                <th>개월</th>
                <th>금리(%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in product.depositoptions_set" :key="option.save_trm">
                <td>{{ option.save_trm }}</td>
                <td>{{ option.intr_rate }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="section">
          <h3>우대 조건</h3>
          <p>{{ product.spcl_cnd }}</p>
        </div>

        <div class="section" v-if="product.spcl_cnd_plus">
          <h3>우대 조건+</h3>
          <p>{{ product.spcl_cnd_plus }}</p>
        </div>

        <div class="section">
          <h3>기타</h3>
          <p>{{ product.etc_note }}</p>
        </div>
        
        <!-- 로그인된 사용자에게만 보이는 가입하기 버튼 -->
        <button v-if="isLoggedIn" @click="joinProduct" class="btn btn-success mt-3">가입하기</button>
        <button @click="goBack" class="btn btn-primary mt-3">뒤로가기</button>

        <!-- 유의사항 추가 -->
        <div class="mt-3 text-muted small">
          <br>
          <p>일반과세의 경우 이자금액의 15.4%가 원천징수되고 비과세 종합저축의 경우 이자소득세가 면제됩니다.</p>
          <p>비과세종합저축은 가입대상자에 한해 5천만원 한도로 적용됩니다.</p>
          <p>관련세법에 따른 세율변경 시 변경된 세율이 적용됩니다.</p>
          <p>본 계산결과는 만기 및 이자금액 계산을 위한 단순 예시로 각 상품별 세제혜택 내용에 따라 달라질 수 있습니다.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const product = ref(null);
const isLoggedIn = ref(!!store.token); // 로그인 상태 확인
const highestInterestOption = ref(null); // 가장 높은 금리를 가진 옵션
const amount = ref(null); // 입력된 금액
const calculatedValue = ref(null); // 계산된 값

const bankLogos = {
  // 은행명과 로고 URL 매핑
  '농협은행주식회사': '/path/to/nh-bank-logo.png',
  '우리은행': '/path/to/woori-bank-logo.png',
  '농협은행주식회사': 'images/image3.png',
  '전북은행': 'images/gb_icon.png',
  '우리은행': 'images/wb_icon.png',
  '광주은행': 'images/gb_icon.png',
  '신한은행': 'images/sh_icon.png',
  '제주은행': 'images/sh_icon.png',
  '부산은행': 'images/bnk_icon.png',
  '경남은행': 'images/bnk_icon.png',
  '한국산업은행': 'images/kdb_icon.png',
  '중소기업은행': 'images/ibk_icon.png',
  '대구은행': 'images/dgb_icon.png',
  '국민은행': 'images/kb_icon.png',
  '하나은행': 'images/hb_icon.png',
  '수협은행': 'images/shb_icon.png',
  '한국스탠다드차타드은행': 'images/sc_icon.png',
  '주식회사 카카오뱅크': 'images/kakao_icon.png',
  '주식회사 케이뱅크': 'images/kbank_icon.png',
  '토스뱅크 주식회사': 'images/toss_icon.png'
};

// 상품 세부 정보를 가져오는 함수
const fetchProductDetails = async () => {
  try {
    const headers = store.token ? { Authorization: `Token ${store.token}` } : {};
    const res = await axios({
      method: 'get',
      url: `${store.API_URL}/financialProducts/deposit-products/${route.params.productId}/`,
      headers,
    });
    product.value = res.data;

    // 가장 높은 금리를 가진 옵션을 찾음
    highestInterestOption.value = res.data.depositoptions_set.reduce((prev, curr) => {
      return (prev.intr_rate2 > curr.intr_rate2) ? prev : curr;
    });
  } catch (err) {
    console.log(err);
  }
};

// 가입하기 버튼 클릭 시 호출되는 함수
const joinProduct = async () => {
  try {
    if (isLoggedIn.value) {
      const headers = { Authorization: `Token ${store.token}` };
      await axios({
        method: 'post',
        url: `${store.API_URL}/financialProducts/api/v1/join-product/`,
        headers,
        data: { productId: route.params.productId },  // Note the change here
      });
      alert('상품 가입이 완료되었습니다.');
      store.getProfile();
    } else {
      alert('로그인이 필요합니다.');
    }
  } catch (err) {
    console.log(err);
    alert('상품 가입에 실패하였습니다.');
  }
};


// 계산하기 버튼 클릭 시 호출되는 함수
const calculate = () => {
  const interestRate = highestInterestOption.value.intr_rate2;
  calculatedValue.value = amount.value * (1 + interestRate / 100);
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchProductDetails();
});

</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  margin-bottom: 20px;
}

.section {
  margin-top: 20px;
}

.rate-box {
  padding: 20px;
  margin-top: 10px;
}

/* 계산기 스타일 */
.input-group {
  width: 250px; /* 입력 필드와 버튼이 한 줄에 정렬되도록 너비 지정 */
  margin: 0 auto; /* 중앙 정렬 */
}

/* 입력 필드와 버튼 크기 조정 */
.form-control-lg {
  height: calc(1.5em + 1rem + 2px);
  font-size: 1.25rem;
  padding: 0.5rem 1rem;
}
.btn-lg {
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
}

/* 유의사항 스타일 */
.text-muted {
  color: #6c757d !important;
}

.small {
  font-size: 0.875em;
}
</style>
