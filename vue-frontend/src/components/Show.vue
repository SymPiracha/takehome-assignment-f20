<template>
  <!-- PART 4: Add your code here -->
  <div class="flex-box">
    <div class="show-box">
      <p class="show-name"> {{name}} </p>
      <Counter v-bind:count="episodes_seen">
      </Counter>
    </div>
  </div>
</template>

<script>
// PART 4: Add your code here
import Counter from './Counter';
export default {
  components: {
    Counter
  },
  props: {
    name: String,
    id: Number,
    episodes_seen: Number
  }
};
</script>

<style scoped>
  .show-box {
    background-color: #D0D0D0;
    margin-bottom: 30px;
  }
  .show-name {
    font-weight:bold;
  }
</style>

