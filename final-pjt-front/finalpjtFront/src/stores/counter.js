
/////////////민준이형///////////////

import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([]);
  const API_URL = 'http://127.0.0.1:8000';
  const token = ref(null);
  const products = ref([]); // 제품 목록을 저장할 ref 추가
  const profile = ref({}); // 프로필 정보를 객체로 변경
  const userId = ref(null); // 사용자 ID 저장

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const router = useRouter();

  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      articles.value = response.data;
      console.log(response.data.article)
    })
    .catch(error => {
      console.log(error);
    });
  };


  const signUp = function (payload) {
    const { username, password1, password2, nickname, age, gender, salary } = payload;

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: { username, password1, password2, nickname, age, gender, salary }
    })
    .then((response) => {
      console.log('회원가입 성공!');
      const password = password1;
      logIn({ username, password });
    })
    .catch((error) => {
      console.log(error);
    });
  };

  const logIn = function (payload) {
    const { username, password } = payload;
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { username, password }
    })
    .then((response) => {
      token.value = response.data.key;
      router.push({ name: 'home' });
      // window.location.reload()
      getProfile()
    })
    .catch((error) => {
      console.log(error);
    });
  };

  // 금융 상품을 가져오는 함수
  const getProduct = function (type, keyword) {
    axios({
      method: 'get',
      url: `${API_URL}/financialProducts/deposit-products/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      params: { type, keyword }
    })
    .then(res => {
      products.value = res.data;
    })
    .catch(error => {
      console.log(error);
    });
  };


  // 프로필을 가져오는 함수
  const getProfile = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      profile.value = response.data;
      console.log(response.data)
    })
    .catch(error => {
      console.log(error);
    });
  };

  const LogOut = function () {
    token.value = null;
    console.log(token.value)
    console.log('로그아웃 완료')
  }

  const deleteProfile = function () {
    axios({
      method: 'delete', // HTTP 메소드
      url: 'http://127.0.0.1:8000/user/delete/', // 회원 탈퇴 API 경로
      headers: {
        Authorization: `Token ${token.value}`, // 필요한 경우 인증 토큰 추가
      },
    })
    .then(response => {
      alert("프로필이 삭제되었습니다.");
      LogOut()
      router.push({ name: 'home' });
      console.log(response.data); // 성공 응답 처리
      // 회원 탈퇴 성공 후 로직, 예: 로그인 페이지로 이동
    })
    .catch(error => {
      console.error('회원 탈퇴 중 오류 발생:', error);
      // 오류 처리 로직, 예: 사용자에게 오류 메시지 표시
    });
  }
  const joinProduct = async function (productId) {
    if (!isLogin.value) {
      alert('로그인이 필요합니다.');
      router.push({ name: 'login' });
      return;
    }
  
    try {
      await axios({
        method: 'post',
        url: `${API_URL}/api/v1/join-product/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: {
          productId: productId,  // 변경된 부분
        },
        
      });
      alert('상품에 가입되었습니다!');
      store.getProfile(); // 가입 후 프로필 정보 갱신
      console.log(productId.data)
    } catch (err) {
      console.log(err);
      alert('가입에 실패했습니다. 다시 시도해주세요.');
    }
  };


  return { articles, API_URL, getArticles, signUp, logIn, token, isLogin, products, getProduct, profile, getProfile, LogOut, deleteProfile, joinProduct };
}, { persist: true });