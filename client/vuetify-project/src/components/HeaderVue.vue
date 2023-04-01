<template>
  <v-toolbar class="bg-grey">
    <div class="px-2"><v-icon icon="mdi-earth"></v-icon></div>
    <v-toolbar-title class="mx-0">Уголок лингвистики</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn flat class="bg-pink-lighten-2">Тренировка частей речи</v-btn>
      <v-btn flat class="bg-pink 400">Совпадения по NY Times</v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
export default {
  name: "Header",
  data: function () {
    return {
      title: "Уголок лингвистики",
    }
  }
}

</script>