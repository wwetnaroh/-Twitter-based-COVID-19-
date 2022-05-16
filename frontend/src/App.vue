<template>
  <div id="app">
    <router-view :key="$route"/>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {}
}
</script>

<style>
html,body,#app{
  margin: 0;
  height: 100%;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
