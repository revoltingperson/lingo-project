<template>
  <v-card variant="outlined" width="1000">
    <template v-slot:title>
      <div class="text-center">Exercise</div>
      <div v-if="buttonsInfo != null" class="text-subtitle-1 text-center">Select the words which can be/are 
      <span class="font-weight-black">{{ this.posNow }}s</span>
      </div>
    </template>
    <template v-slot:text>
      <dot-loader v-if="!buttonsInfo" class="d-flex justify-center"></dot-loader>
      <div v-if="buttonsInfo" class="d-flex justify-space-evenly flex-wrap">
        <v-btn v-for="(item, index) in buttonsInfo" :key="index" @click="validateClick(index)" :color="item.buttonClr"
          size="small" class="text-white mx-2 my-2">{{ item.word }}</v-btn>
      </div>
      <div class="text-center mt-5" v-if="gameFinished"> {{ finalStatement }} <v-btn @click="makeNewRequest"
          size="x-small" color="#9575CD" class="text-white">Generate new</v-btn></div>
    </template>
  </v-card>
</template>

<script>
import axios from 'axios';
import DotLoader from './DotLoader.vue'
export default {
  data() {
    return {
      wordsToReq: 7,
      gameFinished: false,
      finalStatement: "",
      correctOptions: 0,
      userCorrect: 0,
      posNow: null,
      buttonStd: '#9575CD',
      buttonWrong: '#a31217',
      buttonCorrect: '#52cc47',
      buttonsInfo: null,
    }
  },
  methods: {
    validateClick(btnIdx) {
      let currentBtn = this.buttonsInfo[btnIdx];
      this.buttonsInfo.forEach(el => console.log(el))
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
      if (currentBtn.pos.includes(this.posNow)) {
        currentBtn.buttonClr = this.buttonCorrect
        return true
      }
      currentBtn.buttonClr = this.buttonWrong
      return false
    },
    getTotalValidOptions() {
      if (this.buttonsInfo) {
        this.buttonsInfo.forEach(el => (el.pos.includes(this.posNow)) ? this.correctOptions++ : el)
      }
    },
    makeNewRequest() {
      this.gameFinished = false
      this.buttonsInfo = null
      this.posNow = null
      axios.get(`/get-new-tasks/`,
      { params: { 'word_count': this.wordsToReq } })
        .then(response => {
          this.buttonsInfo = response.data.set;
          this.posNow = response.data.target
          this.buttonsInfo.forEach(el => {
            el.buttonClr = this.buttonStd
            el.disabled = false
          })
          this.getTotalValidOptions()

        })
        .catch(error => {
          console.log(error);
        });

    }
  },
  mounted() {
    this.makeNewRequest()
  },
  components: {
    DotLoader
  }
}

</script>

<style>
.option {
  background-color: darksalmon;
  color: greenyellow;
}
</style>