<script setup></script>

<template>
  <div class="OverlayElement">
    <slot></slot>
  </div>
</template>

<style scoped>
.OverlayElement {
  margin: 0 auto 1em auto;
  padding: 0.5em 1em;
  border-radius: 1em;
  background-color: var(--ctp-mocha-overlay2);
  color: var(--ctp-mocha-base);
}
</style>
