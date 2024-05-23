<template>
  <div class="container mt-5">
    <h2 class="mb-4">가입한 금융 상품</h2>
    <div class="row">
      <div class="col-md-4 mb-3" v-for="product in joinedProducts" :key="product.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-3">{{ product.fin_prdt_nm }} ({{ product.kor_co_nm }})</h5>
            <p class="card-text mb-1">{{ product.etc_note }}</p>
            <p class="card-text mb-1">가입 방법: {{ product.join_way }}</p>
            <p class="card-text mb-1">특별 조건: {{ product.spcl_cnd }}</p>
            <button class="btn btn-danger mt-3" @click="cancelSubscription(product.id)">가입 취소</button>
          </div>
        </div>
      </div>
      <div class="col-md-12" v-if="joinedProducts.length === 0">
        <p>가입한 상품이 없습니다.</p>
      </div>
    </div>
    <div v-if="joinedProducts.length > 0" class="chart-container">
      <BarChart :options="chartOptions" :data="chartData" v-if="chartReady"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import colors from 'vuetify/lib/util/colors';

export default {
  setup() {
    const store = useCounterStore();
    const joinedProducts = ref([]);
    const chartReady = ref(false); // 차트 준비 상태 추가
    const chartOptions = ref({
      plugins: {
        title: {
          display: true,
          text: `${store.profile.username}님의 가입한 상품 금리`,
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
          ticks: {
            maxRotation: 30,
            minRotation: 0,
            font: {
              size: 12,
            },
          },
        },
        y: {
          beginAtZero: true,
          suggestedMax: 8,
        },
      },
    });

    const chartData = ref({
      labels: [],
      datasets: [
        {
          label: '저축 금리',
          data: [],
          backgroundColor: '#1089FF',
          stack: 'Stack 0',
        },
        {
          label: '최고 우대 금리',
          data: [],
          backgroundColor: colors.red.accent2,
          stack: 'Stack 1',
        },
      ],
    });

    const fetchJoinedProducts = async () => {
      const userId = store.profile.pk;

      try {
        const response = await axios.get(`${store.API_URL}/profile/${userId}/`);
        joinedProducts.value = response.data.joinedProducts;

        const depositOptionsPromises = joinedProducts.value.map(product => {
          return axios.get(`${store.API_URL}/financialProducts/deposit-products/${product.id}/`);
        });

        const depositOptionsResponses = await Promise.all(depositOptionsPromises);

        chartData.value.labels = joinedProducts.value.map(product => product.fin_prdt_nm);
        chartData.value.datasets[0].data = joinedProducts.value.map((product, index) => {
          const depositOptions = depositOptionsResponses[index].data.depositoptions_set;
          return depositOptions && depositOptions.length > 0 ? depositOptions[0].intr_rate : 0;
        });
        chartData.value.datasets[1].data = joinedProducts.value.map((product, index) => {
          const depositOptions = depositOptionsResponses[index].data.depositoptions_set;
          return depositOptions && depositOptions.length > 0 ? depositOptions[0].intr_rate2 : 0;
        });

        console.log("차트 데이터:", chartData.value);
        chartReady.value = true; // 데이터 로드 완료 후 차트 준비 상태 변경
      } catch (error) {
        console.error('Error fetching joined products:', error);
      }
    };

    const cancelSubscription = async (product_id) => {
      try {
        await axios.delete(`${store.API_URL}/financialProducts/delete-join-product/${parseInt(product_id)}/`, {
          headers: {
            'Authorization': `Token ${store.token}`
          }
        });
        fetchJoinedProducts();
        window.location.reload();
      } catch (error) {
        console.error('Error cancelling subscription:', error);
      }
    };

    onMounted(() => {
      fetchJoinedProducts();
    });

    return {
      joinedProducts,
      chartOptions,
      chartData,
      chartReady, // chartReady 추가
      cancelSubscription,
    };
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #e6e6e6;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.card-body {
  padding: 15px;
}

.card-title {
  color: #333;
  font-size: 1rem;
}

.card-text {
  color: #666;
  font-size: 0.875rem;
}

.btn {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.chart-container {
  position: relative;
  margin-top: 20px;
  height: 400px; /* 차트 높이 설정 */
  width: 100%; /* 차트 너비 설정 */
}
</style>