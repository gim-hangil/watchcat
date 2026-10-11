<script setup>
import { onMounted, ref } from "vue";
import SafetyBadge from "@/components/SafetyBadge.vue";
import SurfaceElement from "@/components/SurfaceElement.vue";
/* load week data from the local storage and request safety data to the server. */
const risks = ref([]);

onMounted(async () => {
  try {
    const res = await fetch("/api/risk");
    const data = await res.json();
    risks.value = data;
  } catch (err) {
    console.error(err.message);
  }
});
</script>

<template>
  <SurfaceElement class="CurrentDetails">
    <div class="title">
      <h3>위험성 순위</h3>
    </div>
    <div :key="risk.job" v-for="risk in risks" class="info">
      {{ risk.job }}: <SafetyBadge :level="risk.level" />
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
