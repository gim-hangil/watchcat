<script setup>
import SafetyBadge from "@/components/SafetyBadge.vue";
import SurfaceElement from "@/components/SurfaceElement.vue";

const props = defineProps({
  week: Array,
  station_id: Number,
  risks: Array,
});
</script>

<template>
  <SurfaceElement class="CurrentDetails">
    <div class="title">
      <h3>위험성 순위</h3>
    </div>
    <div :key="risk.job" v-for="(risk, idx) in props.risks" class="info">
      {{ idx + 1 }}. {{ risk.job }}: <SafetyBadge :level="risk.level" />
    </div>
  </SurfaceElement>
</template>

<style scoped>
.CurrentDetails > * {
  margin-bottom: 1em;
}

.CurrentDetails > *:last-child {
  margin-bottom: 0;
}

.title {
  text-align: center;
}
</style>
