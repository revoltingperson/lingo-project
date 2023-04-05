<template>
  <v-card variant="outlined" width="1000">
    <template v-slot:title>
      <div class="text-center">Exercise</div>
      <div class="text-subtitle-1 text-center">Select the words which can be/are {{ this.categoryNow }}s</div>
    </template>
    <template v-slot:text>
      <div class="d-flex justify-space-evenly flex-wrap">
        <v-btn v-for="(item, index) in buttonsInfo" :key="index" @click="validateClick(index)" :color="item.buttonClr"
          size="small" class="mx-2 my-2">{{ item.word }}</v-btn>
      </div>
      <div class="text-center mt-5" v-if="gameFinished"> {{ finalStatement }} <v-btn @click="makeNewRequest" size="x-small">Generate new</v-btn></div>
    </template>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      gameFinished: false,
      finalStatement: "",
      correctOptions: 0,
      userCorrect: 0,
      categoryNow: "noun",
      buttonStd: '#c3ebfa',
      buttonWrong: '#a31217',
      buttonCorrect: '#52cc47',
      buttonsInfo: [
        { word: "inform", pos: "verb", buttonClr: this.buttonStd, disabled: false },
        { word: "get", pos: "verb", buttonClr: this.buttonStd, disabled: false },
        { word: "lose", pos: "verb", buttonClr: this.buttonStd, disabled: false },
        { word: "transportation", pos: "noun", buttonClr: this.buttonStd, disabled: false },
        { word: "beauty", pos: "noun", buttonClr: this.buttonStd, disabled: false },
        { word: "position", pos: "noun", buttonClr: this.buttonStd, disabled: false },
        { word: "demolish", pos: "verb", buttonClr: this.buttonStd, disabled: false },
      ],
    }
  },
  methods: {
    validateClick(btnIdx) {
      let currentBtn = this.buttonsInfo[btnIdx];
      if (currentBtn.disabled) {
        return
      }
      if (!this.changeBtnColor(currentBtn)) {
        this.buttonsInfo.forEach(el => this.changeBtnColor(el))
        this.gameFinished = true
        this.finalStatement = "Sorry! You've lost"
      } else {
        this.userCorrect++;
      }
      if (this.userCorrect === this.correctOptions) {
        this.buttonsInfo.forEach(el => el.disabled = true)
        this.gameFinished = true
        this.finalStatement = "Congratulations! You aced it!"
      }
    },
    changeBtnColor(currentBtn) {
      currentBtn.disabled = true
      if (currentBtn.pos === this.categoryNow) {
        currentBtn.buttonClr = this.buttonCorrect
        return true
      }
      currentBtn.buttonClr = this.buttonWrong
      return false
    },
    getTotalValidOptions() {
      this.buttonsInfo.forEach(el => (el.pos === this.categoryNow) ? this.correctOptions++ : el)
    },
    makeNewRequest() {
      console.log("making new request");
    }
  },
  mounted() {
    this.getTotalValidOptions();
  }
}

</script>

<style>
.option {
  background-color: darksalmon;
  color: greenyellow;
}
</style>