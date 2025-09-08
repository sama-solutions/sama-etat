<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Styles globaux déjà définis dans neumorphic.css */
#app {
  min-height: 100vh;
  background: var(--bg-primary);
}
</style>