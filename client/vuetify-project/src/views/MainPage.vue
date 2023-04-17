<template>
  <section>
    <v-parallax :src="mainImage" class="image-container w-100">
      <div class="d-flex fill-height flex-column justify-center align-center text-white">
        <h4 class="text-orange subheading">
          Здесь вы найдете интересные материалы для английского языка
        </h4>
      </div>
    </v-parallax>
  </section>
  <section class="bg-grey-lighten-2">
    <v-container class="bg-grey-lighten-2">
      <v-card class="flex">
        <v-card-text>
        </v-card-text>
        <v-card-title class="title">
          <div class="text-h4">Тренажер частей речи</div>
        </v-card-title>
        <v-container>
          <v-card-text>
            Каждое слово, которое вы произносите в предложении, относится к определенной группе. Эти группы и называются
            частями речи (parts of speech).

            Кроме этого, каждое слово выполняет свою функцию в предложении. По большому счету, все эти понятия нам знакомы
            еще
            со школьной скамьи. Но в разрезе частей речи существует разница между русским и английским языком.

            Части речи в английском языке являются более обширным понятием. В английском намного шире переходные зоны, где
            границы между частями речи не просто размыты, а стёрты.
          </v-card-text>
        </v-container>

        <v-card-title class="title">
          <div class="h2 text-center">Классификация</div>
        </v-card-title>
        <v-card-text>

          <div class="d-flex align-start justify-center flex">

            <v-card class="bg-lime-lighten-5 mx-10" width="400">
              <template v-slot:title>
                Знаменательные
              </template>
              <template v-slot:text>
                <ul>
                  <li>существительное (noun)</li>
                  <li>глагол (verb)</li>
                  <li>прилагательное (adjective)</li>
                  <li>наречие (adverb)</li>
                  <li>местоимение (pronoun)</li>
                  <li>числительное (numeral)</li>
                </ul>
              </template>
            </v-card>
            <v-card class="bg-lime-lighten-5 mx-10" width="400">
              <template v-slot:title>
                Служебные
              </template>

              <template v-slot:text>
                <ul>
                  <li>союз (conjunction)</li>
                  <li>предлог (preposition)</li>
                  <li>частица (particle)</li>
                  <li>артикль (article)</li>
                  <li>междометие (interjection)</li>
                </ul>
              </template>
            </v-card>
          </div>
        </v-card-text>
      <div class="d-flex justify-center flex py-10">
        <parts-of-speech/>
      </div>

      </v-card>
    </v-container>


  </section>
</template>

<script>
import PartsOfSpeech from '@/components/PartsOfSpeech.vue';
export default {
  setup() {
      
  },
  data() {
    return {
      mainImage: '../../src/assets/main_image.jpg',
    }
  },
  components: {
    PartsOfSpeech
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
