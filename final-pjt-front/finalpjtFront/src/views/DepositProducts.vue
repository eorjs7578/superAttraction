<template>
  <div id="app" class="container">
    <div class="my-3 d-flex align-items-center justify-content-center">
      <RouterLink class="nav-link" :to="{ name: 'installmentSavingProducts' }">정기 적금</RouterLink>
      <span class="separator">|</span>
      <RouterLink class="nav-link" :to="{ name: 'DepositProducts' }">정기 예금</RouterLink>
    </div>

    <h1 class="my-4 text-center">정기예금</h1>
    <div class="card mb-4">
      <div class="card-header bg-custom text-white">검색하기</div>
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="bank" class="form-label">은행을 선택하세요:</label>
            <div>
              <select @change="fetchProducts" v-model="selectedBank" id="bank" class="form-select">
                <option value="">전체은행</option>
                <option v-for="bank in banks" :value="bank" :key="bank">{{ bank }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredProducts.length">
      <table class="table table-bordered table-hover table-sm">
        <thead class="table-light">
          <tr>
            <th class="text-center">금융회사명</th>
            <th class="text-center">상품명</th>
            <th v-for="month in months" :key="month" class="text-center">{{ month }}개월 금리</th>
            <th class="text-center">비고</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
            <td class="text-truncate" style="max-width: 150px;" :title="product.kor_co_nm">
              <img :src="bankLogos[product.kor_co_nm]" alt="" class="bank-logo">
              {{ product.kor_co_nm }}
            </td>
            <td class="text-truncate" style="max-width: 150px;" :title="product.fin_prdt_nm">{{ product.fin_prdt_nm }}</td>
            <td v-for="month in months" :key="month" class="text-center">
              <template v-if="product.depositoptions_set.find(option => option.save_trm === month)">
                {{ product.depositoptions_set.find(option => option.save_trm === month).intr_rate }}%
              </template>
              <template v-else>-</template>
            </td>
            <td class="text-center">
              <RouterLink :to="{ name: 'DepositProductDetail', params: { productId: product.id } }">
                <button class="btn btn-custom btn-sm">상세</button>
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

export default {
  setup() {
    const store = useCounterStore();
    const route = useRoute();
    const selectedBank = ref('');
    const banks = ref([]);
    const months = ref([6, 12, 24, 36]); // 월 수

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

    const fetchProducts = async () => {
      try {
        await store.getProduct('예금');
        updateBanks();
      } catch (error) {
        console.error('Error fetching deposit products:', error);
      }
    };

    const updateBanks = () => {
      const bankNames = new Set(store.products.map(product => product.kor_co_nm));
      banks.value = Array.from(bankNames);
    };

    const filteredProducts = computed(() => {
      let result = store.products;
      if (selectedBank.value) {
        result = result.filter(product => product.kor_co_nm === selectedBank.value);
      }
      return result;
    });

    onMounted(() => {
      selectedBank.value = route.query.bank || '';
      fetchProducts();
    });

    watch(route, (newRoute) => {
      if (newRoute.query.bank !== selectedBank.value) {
        selectedBank.value = newRoute.query.bank || '';
      }
    });

    return {
      selectedBank,
      banks,
      store,
      filteredProducts,
      fetchProducts,
      months,
      bankLogos,
    };
  }
};
</script>

<style scoped>
#app {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.my-3 {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-link {
  text-decoration: none;
  color: black;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #379cb6;
}

.separator {
  margin: 0 5px;
  color: black;
}

.card-header {
  background-color: #379cb6;
  color: white;
}

.btn-custom {
  background-color: #379cb6;
  color: white;
  font-weight: bold;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-decoration: none;
}

.btn-custom:hover {
  background-color: darken(#379cb6, 10%);
}

.table {
  width: 100%;
  margin-bottom: 1rem;
  color: #212529;
  border-collapse: separate;
  border-spacing: 0;
}

.table th,
.table td {
  padding: 0.5rem;
  vertical-align: middle;
  border-top: 1px solid #dee2e6;
}

.table-sm th,
.table-sm td {
  padding: 0.3rem;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.table-bordered th,
.table-bordered td {
  border: 1px solid #dee2e6;
}

.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}

.table-light {
  background-color: #f8f9fa;
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bank-logo {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}

.text-center {
  text-align: center;
}
</style>
