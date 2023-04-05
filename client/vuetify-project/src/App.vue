<template>
  <v-app>
    <div class="main-container">
      <HeaderVue />
      <div class="content">
        <RouterView />
      </div>
    </div>
    <FooterVue />
  </v-app>
</template>

<script>
import HeaderVue from "./components/HeaderVue.vue"
import FooterVue from "./components/FooterVue.vue"

export default {
  data() {
    return {
      
    }
  },
  components: {
    HeaderVue,
    FooterVue

  }
}
</script>

<style>
.main-container {
  min-height: 92%;
  margin-bottom: 0px;
}

.content {
  padding-bottom: 0px;
  min-height: 100%;
  margin: 0 auto 0px;
}
</style>