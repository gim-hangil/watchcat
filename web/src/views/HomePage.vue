<script setup>
import CurrentLevel from "@/components/CurrentLevel.vue";
import SafetyStatus from "@/components/SafetyStatus.vue";
import OverlayElement from "@/components/OverlayElement.vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});
</script>

<template>
  <div class="HomePage">
    <CurrentLevel :week="props.week" :station_id="props.station_id" />
    <SafetyStatus :week="props.week" :station_id="props.station_id" />
    <RouterLink class="nav-link" to="/details">
      <OverlayElement>세부 현황 보러가기</OverlayElement>
    </RouterLink>
    <RouterLink class="nav-link" to="/forecast">
      <OverlayElement>위험성 예보 확인하기</OverlayElement>
    </RouterLink>
  </div>
</template>

<style scoped>
.HomePage > * {
  margin-bottom: 1rem;
}
.nav-link {
  text-decoration: none;
  text-align: center;
}
</style>
