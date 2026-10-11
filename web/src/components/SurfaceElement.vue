<script setup></script>

<template>
  <div class="SurfaceElement">
    <slot></slot>
  </div>
</template>

<style scoped>
.SurfaceElement {
  margin: 0 auto 1em auto;
  padding: 0.5em 1em;
  border-radius: 1em;
  background-color: var(--ctp-mocha-surface1);
}
</style>
