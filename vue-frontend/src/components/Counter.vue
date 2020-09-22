<template>
  <div>
    <p>I'm a Counter!</p>
    <p>Current Count: {{this.count}} </p>
    <button class="btn" v-on:click="increment">Increment</button>
    <button class="btn" v-on:click="decrement">Decrement</button>
  </div>
</template>

<script>
export default {
  name: "Counter",
  props: {
    count: Number
  },
  data() {
    return {
      count: 0
    };
  },
  methods: {
    increment() {
      this.count = this.count + 1;
    },
    decrement() {
      this.count = this.count - 1;
    }
  }
};
</script>

<style scoped>
  .btn {
    color: whitesmoke;
    background: #41B883;
    border-radius: 50px;
  }

</style>

