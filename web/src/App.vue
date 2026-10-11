<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();

const station_id = ref(0);
const week = ref([]);

onMounted(() => {
  loadLocalStorage();
});

function loadLocalStorage() {
  try {
    station_id.value = JSON.parse(localStorage.getItem("station_id")) || 0;
    week.value = JSON.parse(localStorage.getItem("week")) || [0, 0, 0, 0, 0];
  } catch {
    console.error(
      "Error loading data from localStorage. Initializing with default values.",
    );
    station_id.value = 0;
    week.value = [0, 0, 0, 0, 0];
  } finally {
    localStorage.setItem("station_id", JSON.stringify(station_id.value));
    localStorage.setItem("week", JSON.stringify(week.value));
  }
}
</script>

<template>
  <div class="App">
    <div class="title">
      <h1>워치캣! 안전 지킴이</h1>
    </div>
    <main>
      <RouterView
        @update="loadLocalStorage()"
        :station_id="station_id"
        :week="week"
      />
    </main>
    <footer>
      <RouterLink v-if="route.name !== 'home'" to="/">홈으로</RouterLink>
      <RouterLink to="/accident">사고등록</RouterLink>
      <RouterLink to="/config">설정</RouterLink>
    </footer>
  </div>
</template>

<style scoped>
.title {
  text-align: center;
  margin: 0 auto 1em auto;
}

footer {
  display: flex;
  justify-content: space-evenly;
}
</style>
