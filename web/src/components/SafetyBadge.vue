<script setup>
const props = defineProps({
  level: Number,
});

const COLORS = ["green", "yellow", "red"];
const LABELS = ["안전", "조심", "위험"];
</script>

<template>
  <span :class="['badge', COLORS[props.level]]">{{ LABELS[props.level] }}</span>
</template>

<style scoped>
.badge {
  font-family: "NanumGothicBold";
  border-width: 1px;
  border-style: solid;
  border-radius: 2em;
  padding: 2px 0.5em;
}

.green {
  color: var(--ctp-mocha-green);
  background-color: rgba(var(--ctp-mocha-green-rgb) / 0.2);
  border-color: var(--ctp-mocha-green);
}

.red {
  color: var(--ctp-mocha-red);
  background-color: rgba(var(--ctp-mocha-red-rgb) / 0.2);
  border-color: var(--ctp-mocha-red);
}

.yellow {
  color: var(--ctp-mocha-yellow);
  background-color: rgba(var(--ctp-mocha-yellow-rgb) / 0.2);
  border-color: var(--ctp-mocha-yellow);
}
</style>
