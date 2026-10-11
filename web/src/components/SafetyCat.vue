<script setup>
import CatGood from "@/assets/cat_good.svg";
import CatWarning from "@/assets/cat_warning.svg";
import CatDanger from "@/assets/cat_danger.svg";

const props = defineProps({
  level: Number,
});

const LOGO = [CatGood, CatWarning, CatDanger];
</script>

<template>
  <div class="CatLogo">
    <img class="icon" :src="LOGO[props.level]" />
  </div>
</template>

<style scoped>
.CatLogo {
  text-align: center;
  margin: 0 auto 1em auto;
}

.icon {
  border-radius: 100%;
  border: 3px solid var(--ctp-mocha-surface1);
  width: 90%;
  max-width: 200px;
}
</style>
