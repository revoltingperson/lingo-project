<template>
  <section>
    <v-parallax :src="mainImage" class="image-container w-100">
      <div class="d-flex flex-column justify-center align-center text-white">
        <h1 class="text-h2 text-orange-lighten-3 mb-4">
          Добро пожаловать на сайт!
        </h1>
        <h4 class="text-orange-lighten-3 subheading">
          Здесь вы найдете интересные материалы для английского языка
        </h4>
      </div>
    </v-parallax>
  </section>
  <section>
      <v-card class="flex">
        <v-card-text>
        </v-card-text>
        <v-card-title class="title">
          <div class="headline text-xs-center">Тренажер частей речи</div>
        </v-card-title>
        <v-card-text>
          Show your stuff to the whole community of Endorfine not only to your mum or your friends. We love making good
          content viral. In this moment Endorfine is used by artists who are not famous but that want to share their works
          to the world. Unfortunately with other social networks this is hard, slow and sometime expensive.          Show your stuff to the whole community of Endorfine not only to your mum or your friends. We love making good
          content viral.
        </v-card-text>
      </v-card>
  </section>
</template>

<script>
export default {
  data() {
    return {
      mainImage: '../../src/assets/main_image.jpg',
    }
  }
}
</script>

<style>
.image-container {
  height: 700px;
}
.title {
  text-align: center;
  display: block;
  margin-bottom: 10px;
}
</style>
