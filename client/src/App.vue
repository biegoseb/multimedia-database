<template>
  <div
    class="d-flex flex-column align-items-center justify-content-center mt-5"
  >
    <h1
      style="color: #2d2d2d; font-family: 'Teko', sans-serif; font-size:3rem;"
    >
      Multimedia Browser
    </h1>
    <br />
    <div class="container">
      <Browser />
    </div>
  </div>
</template>

<script>
import Browser from "./components/Browser.vue";
export default {
  name: "App",
  components: {
    Browser,
  },
  data: () => ({}),
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Teko:wght@500&display=swap");
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
