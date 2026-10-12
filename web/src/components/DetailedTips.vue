<script setup>
import { ref, watch } from "vue";
import SurfaceElement from "@/components/SurfaceElement.vue";

const props = defineProps({
  week: Array,
  station_id: Number,
  risks: Array,
});
const tips = ref([]);

watch(
  () => props.risks,
  async () => {
    tips.value = [];
    for (let risk of props.risks) {
      tips.value.push(...(await getTips(risk.id)));
    }
  },
);

async function getTips(accident_id) {
  try {
    const res = await fetch(`/api/tip/${accident_id}`);
    const data = await res.json();
    return [data[Math.floor(Math.random() * data.length)]];
  } catch (err) {
    console.error(err.message);
    return [];
  }
}
</script>

<template>
  <SurfaceElement class="DetailedTips">
    <div class="title">
      <h3>안전 팁!</h3>
    </div>
    <div class="tip" :key="tip.tip" v-for="tip in tips">
      {{ tip.tip }}
    </div>
  </SurfaceElement>
</template>

<style scoped>
.DetailedTips > * {
  margin-bottom: 1em;
}

.DetailedTips > *:last-child {
  margin-bottom: 0;
}

.title {
  text-align: center;
}
</style>
