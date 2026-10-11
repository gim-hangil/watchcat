<script setup>
import { ref, onMounted } from "vue";
import SafetyBadge from "@/components/SafetyBadge.vue";
import SafetyCat from "@/components/SafetyCat.vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});
const level = ref(0);

onMounted(async () => {
  await fetchCurrentLevel();
});

async function fetchCurrentLevel() {
  try {
    const res = await fetch(
      `/api/level/${props.station_id}?week=${props.week[0] || 0}`,
    );
    const data = await res.json();
    level.value = data.level;
  } catch (err) {
    console.error(err.message);
  }
}
</script>

<template>
  <div class="label">
    <h3>지금은 <SafetyBadge :level="level" /></h3>
  </div>
  <SafetyCat :level="level" />
</template>

<style scoped>
.label {
  text-align: center;
  margin: 0 auto 1em auto;
}
</style>
