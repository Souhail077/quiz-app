<template>
  <div class="container" >
    <div v-for="q in question" :key="q.id">
    <h1 class="display-4 mb-4">{{ q.title }}</h1>
    <p class="lead mb-4">{{ q.text }}</p>
    <img :src="q.image" alt="Image" class="mb-4">
    <p class="mb-4">Position: {{ q.position }}</p>
    <p>Réponse : </p>
    <ul class="list-group">
      <li v-for="answer in q.possibleAnswers" :key="answer" class="list-group-item">{{ answer.text }}</li>
    </ul>
  </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'QuestionPage',
  data() {
    return {
      question: {}
    }
  },
  props: {
    id: {
      required: true
    }
  },
  methods: {
    async getQuestion() {
      axios.get(`http://127.0.0.1:5000/questions/${this.id}`, {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
        },
      }).then(({ data }) => {
        console.log(data);
        this.question = data
      });
    }
  },
  created() {
    this.getQuestion()
  }
}
</script>
