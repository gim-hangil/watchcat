<script setup>
import { onMounted, ref } from "vue";
import CurrentDetails from "@/components/CurrentDetails.vue";
import DetailedTips from "@/components/DetailedTips.vue";

const props = defineProps({
  station_id: Number,
  week: Array,
});

const risks = ref([]);

onMounted(async () => {
  try {
    const res = await fetch(`/api/risk?week_id=${props.week[0]}`);
    const data = await res.json();
    risks.value = data;
    console.log("DetailsPage updated to week", props.week[0]);
  } catch (err) {
    console.error(err.message);
  }
});
</script>

<template>
  <div class="DetailsPage">
    <h3>지금의 세부 현황</h3>
    <CurrentDetails
      :week="props.week"
      :station_id="props.station_id"
      :risks="risks"
    />
    <DetailedTips
      :week="props.week"
      :station_id="props.station_id"
      :risks="risks"
    />
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
