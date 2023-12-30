<template>
  <div id="app">
    <TestHehe />
  </div>
</template>

<script>
import TestHehe from './components/TestHehe.vue';

export default {
  name: 'App',
  components: {
    TestHehe
}
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
