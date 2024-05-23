<template>
  <div class="container mt-5">
    <h1 class="mb-4 text-center">환율 계산기</h1>
    <div class="card shadow-sm">
      <div class="card-body">
        <div class="form-group">
          <label for="currency">외국 통화 코드:</label>
          <select v-model="currency" @change="updateCurrencyInfo" id="currency" class="form-control">
            <option disabled value="">통화 코드 선택</option>
            <option v-for="cur in currencies" :key="cur.code" :value="cur.code">{{ cur.name }} ({{ cur.code }})</option>
          </select>
          <div v-if="currentCurrencyInfo" class="bbox mt-3 p-3 bg-light rounded">
            <p><strong>국가:</strong> {{ currentCurrencyInfo.name }}</p>
            <p><strong>통화 코드:</strong> {{ currentCurrencyInfo.code }}</p>
            <p><strong>단위:</strong> {{ currentCurrencyInfo.unit }}</p>
          </div>
        </div>
        <div class="form-group mt-4">
          <label for="foreignAmount">외국 통화 금액:</label>
          <div class="input-group">
            <input v-model="formattedForeignAmount" id="foreignAmount" type="text" class="form-control" placeholder="외국 통화 금액 입력" @input="onForeignAmountInput" />
            <div v-if="currentCurrencyInfo" class="input-group-append">
              <span class="input-group-text unit-width">{{ currentCurrencyInfo.unit }}</span>
            </div>
          </div>
        </div>
        <div>
          <h1 class="equal"> = </h1>
        </div>
        <div class="form-group mt-4">
          <label for="krwAmount">원화 금액 (KRW):</label>
          <div class="input-group">
            <input v-model="formattedKrwAmount" id="krwAmount" type="text" class="form-control" placeholder="KRW 금액 입력" @input="onKrwAmountInput" />
            <div class="input-group-append">
              <span class="input-group-text unit-width">원</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div>
    <br>
    <span class="notice">* 엔화, 인도네시아 루피아는 100단위, 나머지는 모두 1단위</span><br><br>
  </div>

  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
    <path fill="#0099ff" fill-opacity="1" d="M0,128L48,122.7C96,117,192,107,288,106.7C384,107,480,117,576,101.3C672,85,768,43,864,32C960,21,1056,43,1152,58.7C1248,75,1344,85,1392,90.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
  </svg>
</template>
<script>
import { ref, reactive, computed } from 'vue';

export default {
  setup() {
    const currency = ref('');
    const krwAmount = ref(0);
    const foreignAmount = ref(0);
    const exchangeRate = ref(null);
    const currentCurrencyInfo = ref(null);
    const exchangeRateCache = reactive({});
    const currencies = reactive([
      { name: "미국", code: "USD", unit: "달러" },
      { name: "일본", code: "JPY", unit: "엔(100)" },
      { name: "대한민국", code: "KRW", unit: "원" },
      { name: "아랍에미리트", code: "AED", unit: "디르함" },
      { name: "호주", code: "AUD", unit: "달러" },
      { name: "바레인", code: "BHD", unit: "디나르" },
      { name: "브루나이", code: "BND", unit: "달러" },
      { name: "캐나다", code: "CAD", unit: "달러" },
      { name: "스위스", code: "CHF", unit: "프랑" },
      { name: "중국", code: "CNH", unit: "위안화" },
      { name: "덴마크", code: "DKK", unit: "크로네" },
      { name: "유럽", code: "EUR", unit: "유로" },
      { name: "영국", code: "GBP", unit: "파운드" },
      { name: "홍콩", code: "HKD", unit: "달러" },
      { name: "인도네시아", code: "IDR", unit: "루피아(100)" },
      { name: "쿠웨이트", code: "KWD", unit: "디나르" },
      { name: "말레이시아", code: "MYR", unit: "링기트" },
      { name: "노르웨이", code: "NOK", unit: "크로네" },
      { name: "뉴질랜드", code: "NZD", unit: "달러" },
      { name: "사우디", code: "SAR", unit: "리얄" },
      { name: "스웨덴", code: "SEK", unit: "크로나" },
      { name: "싱가포르", code: "SGD", unit: "달러" },
      { name: "태국", code: "THB", unit: "바트" },
    ]);

    const formattedKrwAmount = computed({
      get() {
        return krwAmount.value ? krwAmount.value.toLocaleString() : '';
      },
      set(value) {
        krwAmount.value = value ? parseFloat(value.replace(/,/g, '')) : 0;
      }
    });

    const formattedForeignAmount = computed({
      get() {
        return foreignAmount.value ? foreignAmount.value.toLocaleString() : '';
      },
      set(value) {
        foreignAmount.value = value ? parseFloat(value.replace(/,/g, '')) : 0;
      }
    });

    function updateCurrencyInfo() {
      const found = currencies.find(c => c.code === currency.value);
      currentCurrencyInfo.value = found ? found : null;
      if (!found) {
        exchangeRate.value = null;
      } else {
        fetchExchangeRate().then(rate => {
          exchangeRate.value = rate;
          calculateKrwAmount();
          calculateForeignAmount();
        });
      }
    }

    async function fetchExchangeRate() {
      if (exchangeRateCache[currency.value]) {
        return exchangeRateCache[currency.value];
      }

      const targetCurrency = currency.value === 'JPY' || currency.value === 'IDR'
        ? `${currency.value}(100)`
        : currency.value;
    
      const url = `https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=${import.meta.env.VITE_EXCHANGE_API_KEY}&data=AP01`;
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`API 호출 실패. 응답 코드: ${response.status}`);
        const data = await response.json();
        const rateInfo = data.find(d => d.cur_unit === targetCurrency);
        if (rateInfo) {
          const rate = parseFloat(rateInfo.deal_bas_r.replace(/,/g, ''));
          exchangeRateCache[currency.value] = rate;
          return rate;
        } else {
          return null;
        }
      } catch (error) {
        console.error('[ERROR]', error);
        return null;
      }
    }

    function calculateKrwAmount() {
      if (currency.value && foreignAmount.value > 0 && exchangeRate.value) {
        let rate = exchangeRate.value;
        if (currency.value === 'JPY' || currency.value === 'IDR') {
          rate /= 100; // JPY 또는 IDR인 경우 100으로 나눔
        }
        const result = (foreignAmount.value * rate).toFixed(2);
        krwAmount.value = parseFloat(result);
      } else {
        krwAmount.value = 0;
      }
    }

    function calculateForeignAmount() {
      if (currency.value && krwAmount.value > 0 && exchangeRate.value) {
        let rate = exchangeRate.value;
        if (currency.value === 'JPY' || currency.value === 'IDR') {
          rate /= 100; // JPY 또는 IDR인 경우 100으로 나눔
        }
        const result = (krwAmount.value / rate).toFixed(2);
        foreignAmount.value = parseFloat(result);
      } else {
        foreignAmount.value = 0;
      }
    }

    function onForeignAmountInput(event) {
      formattedForeignAmount.value = event.target.value;
      calculateKrwAmount();
    }

    function onKrwAmountInput(event) {
      formattedKrwAmount.value = event.target.value;
      calculateForeignAmount();
    }

    return { 
      currency, 
      krwAmount, 
      foreignAmount, 
      currentCurrencyInfo, 
      updateCurrencyInfo, 
      calculateKrwAmount, 
      calculateForeignAmount, 
      formattedKrwAmount, 
      formattedForeignAmount, 
      onForeignAmountInput, 
      onKrwAmountInput, 
      currencies
    };
  },
};
</script>

<style scoped>
body {
  background-color: #dde4ee; /* 원하는 배경색으로 변경 */
}

.container {
  max-width: 1000px;
  margin: auto;
  background-color: #ffffff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card {
  border: none;
  border-radius: 15px;
}

.card-body {
  padding: 20px;
}

h1 {
  font-size: 2rem;
  color: #495057;
}

.label {
  font-weight: bold;
  color: #495057;
}

.form-control {
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.input-group-text {
  border-radius: 15px;
  /* background-color: #17a2b8; */
  color: #fff;
  font-weight: bold;
}

.input-group {
  display: flex;
}

.unit-width {
  width: 70px;
  height: 50px;
  text-align: center;
  background-color: #17a2b8;
  color: #fff;
  font-weight: bold;
  border-radius: 0 15px 15px 0;
}

.equal {
  text-align: center;
  font-size: 2rem;
  color: #495057;
}

.bbox {
  text-align: center;
  background-color: #e2e6ea;
  border: 1px solid #dae0e5;
  border-radius: 15px;
  padding: 15px;
  margin-top: 15px;
}

.notice {
  display: block;
  text-align: center;
  color: #6c757d;
  font-size: 0.85rem;
  margin-top: 1rem;
}
</style>