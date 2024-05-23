import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'
import vuetify from './plugins/vuetify'; // Vuetify 플러그인 import
import Chart from 'chart.js/auto'; // Chart.js 플러그인 자동 등록
import { Bar } from 'vue-chartjs';

const app = createApp(App)
const pinia = createPinia()
app.component('BarChart', Bar); // Bar 컴포넌트를 전역 등록

app.use(pinia)
pinia.use(piniaPluginPersistedstate)
// app.use(createPinia())
app.use(vuetify); // Vuetify 플러그인 등록
app.use(router)

app.mount('#app')
