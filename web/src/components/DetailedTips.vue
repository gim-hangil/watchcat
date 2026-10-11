<script setup>
import { onMounted, ref } from "vue";
import SurfaceElement from "@/components/SurfaceElement.vue";
/* load week data from the local storage and request safety data to the server. */
const tips = ref([]);

onMounted(async () => {
  try {
    const res = await fetch("/api/tip");
    const data = await res.json();
    tips.value = data;
  } catch (err) {
    console.error(err.message);
  }
});
</script>

<template>
  <SurfaceElement class="DetailedTips">
    <div class="title">
      <h3>안전 팁!</h3>
    </div>
    <div :key="idx" v-for="(tip, idx) in tips">
      {{ tip }}
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
