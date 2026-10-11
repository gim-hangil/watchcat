<script setup>
import { onMounted, ref } from "vue";
import SafetyBadge from "@/components/SafetyBadge.vue";
const props = defineProps({
  week_id: Number,
  term: Number,
});
const safety = ref({ job: "", level: 0 });

onMounted(async () => {
  await fetchSafety();
});

async function fetchSafety() {
  if (props.week_id !== null && props.week_id !== undefined) {
    const res = await fetch(`/api/forecast?week_id=${props.week_id}`);
    const data = await res.json();
    safety.value = data;
  }
}
</script>

<template>
  <div class="WeekForecast">
    <span v-if="props.week_id"
      >{{ props.term }}주 뒤, {{ safety.job }} 주:
      <SafetyBadge :level="safety.level"
    /></span>
    <span v-else> {{ props.term }}주 뒤: 주차를 설정해주세요.</span>
  </div>
</template>

<style scoped></style>
