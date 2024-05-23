<template>
  <div id="recommendation" class="container">
    <h1 class="my-4">맞춤 금융 상품 추천</h1>
    <div class="card mb-4">
      <div class="card-header">정보 입력</div>
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="preferredBank" class="form-label">선호하는 은행:</label>
            <select v-model="preferredBank" id="preferredBank" class="form-select">
              <option value="">상관없음</option>
              <option v-for="bank in banks" :value="bank" :key="bank">{{ bank }}</option>
            </select>
          </div>
          <div class="col-md-6">
            <label for="minInterestRate" class="form-label">최소 금리 (%):</label>
            <input type="number" class="form-control" id="minInterestRate" v-model.number="minInterestRate">
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="joinMethod" class="form-label">가입 방식:</label>
            <select v-model="joinMethod" id="joinMethod" class="form-select">
              <option value="">상관없음</option>
              <option value="영업점">영업점 방문</option>
              <option value="인터넷">인터넷뱅킹</option>
              <option value="스마트폰">스마트폰</option>
            </select>
          </div>
          <div class="col-md-6">
            <label for="productType" class="form-label">상품 유형:</label>
            <select v-model="productType" id="productType" class="form-select">
              <option value="">모두</option>
              <option value="예금">예금</option>
              <option value="적금">적금</option>
            </select>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-12">
            <button class="btn btn-primary btn-search" @click="filterProducts">조건 검색</button> <!-- Added class -->
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredProducts.length">
      <h2>추천 상품</h2>
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th></th>
            <th>금융회사명</th>
            <th>상품명</th>
            <th>상품 유형</th>
            <th>최고 금리</th>
            <th>가입 방법</th>
            <th>우대 조건</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
            <td>{{ product.dcls_month }}</td>
            <td class="text-truncate" style="max-width: 150px;" :title="product.kor_co_nm">
              <img :src="bankLogos[product.kor_co_nm]" alt="" class="bank-logo">
              {{ product.kor_co_nm }}
            </td>
            <td class="text-truncate" style="max-width: 150px;" :title="product.fin_prdt_nm">{{ product.fin_prdt_nm }}</td>
            <td>
              {{ product.fin_prdt_nm.includes('예금') ? '예금' : 
                (product.fin_prdt_nm.includes('적금') ? '적금' : '기타') }}
            </td>
            <td>{{ getHighestInterestRate(product) }}%</td>
            <td>{{ product.join_way }}</td>
            <td class="text-truncate" style="max-width: 150px;" :title="product.spcl_cnd">{{ product.spcl_cnd }}</td>
            <td>
              <RouterLink :to="{ name: 'DepositProductDetail', params: { productId: product.id } }">
                <button class="btn btn-primary btn-sm">상세</button>
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="isLoading">
      <p>Loading...</p>
    </div>
    <div v-else>
      <p>조건에 맞는 상품이 없습니다.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

export default {
  setup() {
    const allproducts = ref([])
    const store = useCounterStore();
    const preferredBank = ref('');
    const minInterestRate = ref(0);
    const age = ref(null);
    const joinMethod = ref('');
    const productType = ref(''); // 상품 유형 (예금, 적금)
    const isLoading = ref(false);
    const filteredProducts = ref([]); // 필터링된 상품을 저장할 변수

    // 모든 금융 상품을 가져오는 함수
    const getallProduct = function () {
      axios({
        method: 'get',
        url: `${store.API_URL}/financialProducts/deposit-allproducts/`,
        headers: {
          Authorization: `Token ${store.token}`
        },
      })
      .then(response => {
        allproducts.value = response.data; // 상태관리 저장소에 데이터 저장
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
    };

    const banks = computed(() => {
  // store.allproducts가 undefined이거나 배열이 아닌 경우를 처리
  if (!allproducts.value || !Array.isArray(allproducts.value)) {
    return []; // 빈 배열을 반환하여 에러를 방지
  }
  const bankNames = new Set(allproducts.value.map(product => product.kor_co_nm));
  return Array.from(bankNames);
});
  const bankLogos = {
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


      const getHighestInterestRate = (product) => {
      const highestRateOption = product.depositoptions_set.reduce((prev, curr) => {
        return (prev.intr_rate2 > curr.intr_rate2) ? prev : curr;
      });
      return highestRateOption ? highestRateOption.intr_rate2 : 0;
    };

    const filterProducts = () => {
      isLoading.value = true;
      setTimeout(() => {
        const filtered = allproducts.value.filter(product => {
          const matchesBank = preferredBank.value === '' || product.kor_co_nm === preferredBank.value;
          const matchesInterestRate = minInterestRate.value === 0 || getHighestInterestRate(product) >= minInterestRate.value;
          const matchesJoinMethod = joinMethod.value === '' || product.join_way.includes(joinMethod.value);
          const matchesProductType = productType.value === '' || (
            (productType.value === '예금' && product.fin_prdt_nm.includes('예금')) || 
            (productType.value === '적금' && product.fin_prdt_nm.includes('적금'))
          ); // 상품 유형 필터링 (상품명에 '예금' 또는 '적금' 포함 여부 확인)

          return matchesBank && matchesInterestRate && matchesJoinMethod && matchesProductType; 
        });
        filteredProducts.value = filtered; 
        isLoading.value = false;
      }, 500); 
    };

    onMounted(() => {
      getallProduct(); // 컴포넌트가 마운트될 때 모든 상품 가져오기
      console.log(allproducts)
    });

    return {
      banks,
      bankLogos,
      preferredBank,
      minInterestRate,
      age,
      joinMethod,
      productType, // 상품 유형 선택을 위한 변수
      filteredProducts, // 필터링된 상품을 반환합니다.
      getHighestInterestRate,
      filterProducts,
      isLoading,
    };
  },
};
</script>

<style scoped>
/* 추가된 스타일 */
.btn-search {
  background-color: #379cb6;
  border-color: #379cb6;
}

.btn-search:hover {
  background-color: #379cb6;
  border-color: #379cb6;
}

.btn-primary {
  background-color: #379cb6;
  border-color: #379cb6;
}

.btn-primary:hover {
  background-color: #379cb6;
  border-color: #379cb6;
}
.bank-logo {
  width: 20px; /* 원하는 크기로 조정하세요 */
  height: auto; /* 높이를 자동으로 조정하여 비율 유지 */
}

</style>