<template>
  <div class="about">
    <div>
      <form v-if="showForm" @submit.prevent="onSubmit">
        <template v-for="(question, qIndex) in questions">
          <h3>{{ question.title }}</h3>
          <p>{{ question.text }}</p>
          <!-- <template v-if="question.image">
            <img v-bind:src="'data:image/jpeg;base64,' + question.image" />
          </template> -->
          <template v-for="(answer, aIndex) in question.possibleAnswers">
            <label>
              <input type="radio" v-bind:value="answer.text" v-bind:name="'question-' + question.id"
                v-model="question.selectedAnswer" @change="selectedAnswerIndexes[qIndex]= aIndex+1">
                {{ aIndex + 1 }}.{{ answer.text }}
            </label>
          </template>
        </template>
        <input type="text" id="playerName" v-model="playerName">
        <button type="submit">Envoyer</button>
      </form>
    </div>
    <div  v-if="!showForm">
      <h3>Bonjour {{ playerName }} Votre score est : {{ numCorrect }}</h3>
      <div v-for="scoreEntry in quizInfos.data.scores" v-bind:key="scoreEntry.date">
        <p>Player name : </p>{{ scoreEntry.playerName }} - <p>Score : </p>{{ scoreEntry.score }}
      </div>
      <button @click="goToHome">Home</button>
    </div>
  </div>
</template>

<script>

import quizApiService from "@/services/QuizApiService";
import axios from "axios";

export default {
  data() {
    return {
      showForm: true,
      questions: [],
      selectedAnswerIndexes : [],
      numCorrect: 0,
      playerName: '',
      quizInfos : {},
    }
  },
  created() {
    try {
      quizApiService.getQuestions().then((data) => {
        this.questions = data.data
      })
    } catch (error) {
      console.error(error)
    }
    for (const question of this.questions) {
      question.selectedAnswer = '';
    }
    try {
      quizApiService.getQuizInfo().then((data) => {
      this.quizInfos = data
    });
    } catch (error) {
      console.error(error)
    }
  },
  methods: {
    async onSubmit() {
      this.questions.forEach(question => {
        question.possibleAnswers.forEach(answer => {
          //this.answers.push(answer.indexOf(question.selectedAnswer))
          if (answer.text === question.selectedAnswer) {
            if (answer.isCorrect) { console.log('Correct!'); this.numCorrect++; }
            else { console.log('Incorrect!') }
          }
        })
        this.showForm = false;
      });
      try {
          // Send the POST request to the Flask server
          const response = await axios.post('http://127.0.0.1:5000/participations', {
            playerName: this.playerName,
            answers: this.selectedAnswerIndexes
          });
          console.log(response.data); // Log the response data
        } catch (error) {
          console.error(error); // Log the error
        };  
    },
    goToHome() {
      this.$router.push('/');
    },
  }
}
</script>