<template>
  <v-footer class="d-flex flex-column wrap px-0 py-0">
    <div class="bg-teal d-flex w-100 align-center px-4">
      <strong>Get connected with us on social networks!</strong>
      <v-btn></v-btn>
    </div>

    <div class="px-4 py-2 bg-black text-center w-100">
      {{ new Date().getFullYear() }} — <strong>Vadim Shakin</strong>
    </div>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",
  data: function () {
  }
}

</script>
<style>

</style>