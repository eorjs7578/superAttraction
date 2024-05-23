<template>
    <div id="app">
      <div id="controls">
        <div class="filter-container">
          <div class="filter-item">
            <label for="city">시/도 선택:</label>
            <select id="city" v-model="selectedCity" @change="updateDistricts">
              <option v-for="city in Object.keys(cityDistricts)" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
          <div class="filter-item">
            <label for="district">구/군 선택:</label>
            <select id="district" v-model="selectedDistrict">
              <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
            </select>
          </div>
          <div class="filter-item">
            <label for="bank">은행 선택:</label>
            <select id="bank" v-model="selectedBank">
              <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
            </select>
          </div>
          <button @click="searchBanks">검색</button>
        </div>
      </div>
      <div id="map"></div>
    </div>
  </template>
  
  <script>
  export default {
    name: "BanksFind",
    data() {
      return {
        map: null,
        markers: [],
        infowindows: [],
        cityDistricts: {
          '서울특별시': ['강남구', '서초구', '송파구', '강동구', '광진구', '중구', '종로구', '용산구', '성북구', '노원구', '마포구'],
          '부산광역시': ['해운대구', '수영구', '동래구', '부산진구', '남구', '사하구', '사상구', '연제구', '중구', '동구'],
          '대구광역시': ['수성구', '달서구', '중구', '동구', '서구', '남구', '북구', '달성군'],
          '인천광역시': ['부평구', '남동구', '연수구', '미추홀구', '서구', '계양구', '강화군', '옹진군'],
          '광주광역시': ['광산구', '북구', '서구', '동구', '남구'],
          '대전광역시': ['유성구', '서구', '동구', '중구', '대덕구'],
          '울산광역시': ['남구', '중구', '동구', '북구', '울주군'],
          '세종특별자치시': ['세종시'],
          '경기도': ['수원시', '용인시', '성남시', '고양시', '안양시', '부천시', '광명시', '평택시', '의정부시', '김포시', '안산시'],
          '강원도': ['춘천시', '원주시', '강릉시', '동해시', '속초시', '철원군', '홍천군', '횡성군', '평창군'],
          '충청북도': ['청주시', '충주시', '제천시', '보은군', '옥천군', '영동군', '괴산군', '증평군', '진천군', '음성군'],
          '충청남도': ['천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시', '당진시', '금산군', '부여군', '서천군'],
          '전라북도': ['전주시', '군산시', '익산시', '정읍시', '남원시', '김제시', '완주군', '진안군', '무주군', '장수군'],
          '전라남도': ['목포시', '여수시', '순천시', '나주시', '광양시', '담양군', '곡성군', '구례군', '고흥군', '보성군', '화순군'],
          '경상북도': ['포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시'],
          '경상남도': ['창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시', '의령군', '함안군', '창녕군'],
          '제주특별자치도': ['제주시', '서귀포시'],
        },
        banks: ['농협은행', '신한은행', '국민은행', '우리은행', '하나은행', '기업은행', 'SC제일은행', '카카오뱅크', '케이뱅크'],
        selectedCity: '',
        selectedDistrict: '',
        selectedBank: '',
        districts: [],
      };
    },
    methods: {
      loadScript() {
        const script = document.createElement("script");
        script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAPS_API_KEY}&libraries=services&autoload=false`;
        script.onload = () => window.kakao.maps.load(this.initMap);
        document.head.appendChild(script);
      },
      initMap() {
        const container = document.getElementById("map");
        const options = {
          center: new window.kakao.maps.LatLng(33.450701, 126.570667),
          level: 3
        };
        this.map = new window.kakao.maps.Map(container, options);
      },
      clearMarkers() {
        this.markers.forEach(marker => marker.setMap(null));
        this.markers = [];
        this.infowindows.forEach(infowindow => infowindow.close());
        this.infowindows = [];
      },
      updateDistricts() {
        this.districts = this.cityDistricts[this.selectedCity] || [];
        this.selectedDistrict = this.districts.length > 0 ? this.districts[0] : '';
      },
      searchBanks() {
        const ps = new window.kakao.maps.services.Places();
        const query = `${this.selectedCity} ${this.selectedDistrict} ${this.selectedBank} 은행`;
  
        ps.keywordSearch(query, (data, status) => {
          if (status === window.kakao.maps.services.Status.OK) {
            this.displayMarkers(data);
          } else {
            console.error('No results found');
          }
        });
      },
      displayMarkers(places) {
        this.clearMarkers();
  
        places.forEach(place => {
          const markerPosition = new window.kakao.maps.LatLng(place.y, place.x);
          const marker = new window.kakao.maps.Marker({
            position: markerPosition,
          });
          marker.setMap(this.map);
          this.markers.push(marker);
  
          const infowindow = new window.kakao.maps.InfoWindow({
            content: `
              <div style="padding-bottom: 30px; padding-left:10px; padding-top: 5px; padding-right:10px; font-size: 15px; font-family: Arial, sans-serif; max-width: 300px; ">
                <strong>${place.place_name}</strong><br>
                <span style="color: #888;">${place.road_address_name || place.address_name}</span><br>
                <a href="https://map.kakao.com/link/to/${place.id}" target="_blank" style="color: #007bff; text-decoration: none;">길찾기</a>
              </div>`,
          });
  
          window.kakao.maps.event.addListener(marker, 'click', () => {
            if (infowindow.getMap()) {
              infowindow.close();
            }
            infowindow.open(this.map, marker);
          });
  
          this.infowindows.push(infowindow);
        });
  
        if (places.length > 0) {
          const firstPlace = places[0];
          const firstPosition = new window.kakao.maps.LatLng(firstPlace.y, firstPlace.x);
          this.map.setCenter(firstPosition);
        }
      }
    },
    mounted() {
      this.loadScript();
      this.selectedCity = Object.keys(this.cityDistricts)[0];
      this.updateDistricts();
      this.selectedBank = this.banks[0];
    },
  }
  </script>
  
  <style scoped>
  #app {
    height: 100vh;
    width: 100vw;
    margin: 0;
    position: relative;
  }
  
  #controls {
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.8);
    padding: 10px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 100;
    display: flex;
    align-items: center;
  }
  
  .filter-container {
    display: flex;
    align-items: center;
  }
  
  .filter-item {
    margin-right: 10px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  
  #controls label {
    margin-bottom: 2px;
    font-weight: bold;
    font-size: 14px;
  }
  
  #controls select,
  #controls button {
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
  }
  
  #controls button {
    background: #379cb6;
    color: white;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  
  #controls button:hover {
    background: #379cb6;
  }
  
  #map {
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
  }
  </style>
  