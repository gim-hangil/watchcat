<script setup>
import CurrentDetails from "@/components/CurrentDetails.vue";
import DetailedTips from "@/components/DetailedTips.vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});
</script>

<template>
  <div class="DetailsPage">
    <h3>지금의 세부 현황</h3>
    <CurrentDetails :week="props.week" :station_id="station_id" />
    <DetailedTips :week="props.week" :station_id="station_id" />
  </div>
</template>

<style scoped>
.DetailsPage > * {
  margin-bottom: 1em;
}

.DetailsPage h3 {
  text-align: center;
}
</style>
