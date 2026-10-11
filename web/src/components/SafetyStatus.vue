<script setup>
import { onMounted, ref } from "vue";
import SafetyBadge from "@/components/SafetyBadge.vue";
import SurfaceElement from "@/components/SurfaceElement.vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});

const most_risk = ref("");
const temperature = ref(0);
const rain = ref(0);
const air = ref(0);

onMounted(async () => {
  try {
    const res = await fetch(
      `/api/level/${props.station_id}/temperature?week_id=${props.week[0] || 0}`,
    );
    const data = await res.json();
    temperature.value = data.level;
  } catch (err) {
    console.error(err.message);
  }
  try {
    const res = await fetch(
      `/api/level/${props.station_id}/rain?week_id=${props.week[0] || 0}`,
    );
    const data = await res.json();
    rain.value = data.level;
  } catch (err) {
    console.error(err.message);
  }
  try {
    const res = await fetch(
      `/api/level/${props.station_id}/air?week_id=${props.week[0] || 0}`,
    );
    const data = await res.json();
    air.value = data.level;
  } catch (err) {
    console.error(err.message);
  }
});
</script>

<template>
  <SurfaceElement class="SafetyStatus">
    <h3 class="title">주요 안전 현황</h3>
    <div class="noti">
      <span>조심해야 할 안전사고: <strong>기동 간 낙상</strong></span>
    </div>
    <div class="info">🔥 온도: <SafetyBadge :level="temperature" /></div>
    <div class="info">🌧 강우: <SafetyBadge :level="rain" /></div>
    <div class="info">😷 공기질: <SafetyBadge :level="air" /></div>
  </SurfaceElement>
</template>

<style scoped>
.SafetyStatus > * {
  margin-bottom: 1em;
}

.SafetyStatus > *:last-child {
  margin-bottom: 0;
}

.title {
  text-align: center;
}
</style>
