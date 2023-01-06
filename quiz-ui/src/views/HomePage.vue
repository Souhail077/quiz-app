<template>
  <div>
    <div v-for="scoreEntry in quizInfos.data.scores" v-bind:key="scoreEntry.date">
      <p>Player name : </p>{{ scoreEntry.playerName }} - <p>Score : </p>{{ scoreEntry.score }}
    </div>
    <div>
      <p>size: {{ quizInfos.data.size }}</p>
    </div>
    <div>
      <router-link to="/quiz-page" class="button">Participer au quiz</router-link>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      quizInfos : {},
    };
  },
  async created() {
		console.log("Composant Home page 'created'");
    try {
      quizApiService.getQuizInfo().then((data) => {
      this.quizInfos = data
    });
    } catch (error) {
      console.error(error)
    }
  }
};
</script>