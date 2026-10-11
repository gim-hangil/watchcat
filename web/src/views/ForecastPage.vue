<script setup>
import SurfaceElement from "@/components/SurfaceElement.vue";
import WeekForcast from "@/components/WeekForecast.vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});
</script>

<template>
  <SurfaceElement class="ForecastPage">
    <div class="title">
      <h3>위험성 순위</h3>
    </div>
    <WeekForcast
      class="item"
      v-for="n in 4"
      :key="props.week[n]"
      :week_id="props.week[n]"
      :term="n"
    />
  </SurfaceElement>
</template>

<style scoped>
.ForecastPage > * {
  margin-bottom: 1em;
}

.ForecastPage > *:last-child {
  margin-bottom: 0;
}

.title {
  text-align: center;
}

.item {
  margin-bottom: 1em;
}
</style>
