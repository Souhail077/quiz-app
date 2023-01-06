<template>
<div>
  <div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Question</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="question in questions" :key="question.id">
          <router-link :to="{name: 'QuestionPage', params:{id:question.id}}">
            <td>{{ question.id }}</td>
            <td>{{ question.text }}</td>
          </router-link>
          <td>
            <button @click="editQuestion(question.id)">Éditer</button>
            <button @click="deleteQuestion(question.id)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button @click="addQuestion">Créer une question</button>
  </div>
</div>
</template>

<script>
import { useRouter } from 'vue-router'
import { ref, reactive } from 'vue'
import quizApiService from "@/services/QuizApiService";

export default {
  name: 'Admin',
  setup() {
    const router = useRouter()
    const questions = reactive([])
    const loading = ref(true)
    async function fetchQuestions() {
      try {
        // set loading to true while the data is being fetched
        loading.value = true
        // fetch the questions from the API
        const response  = await quizApiService.getQuestions()
        // extract the data from the response object
        const data = response.data
        // update the questions array with the data from the API
        questions.splice(0, questions.length, ...data)
      } catch (error) {
        console.error(error)
      } finally {
        // set loading to false once the data has been fetched
        loading.value = false
      }
    }
    
    // call fetchQuestions when the component is created
    fetchQuestions()
        
    function showQuestion(id) {
      // show the question with the specified ID
      router.push(`/questions/${id}`)
    }

    async function addQuestion() {
      // add a new question to the table
      try {
        this.$router.push('/addQuestion')
      } catch (error) {
        console.error(error)
      }
    }

    async function editQuestion(id) {
      // edit the question with the specified ID
      try {
        const response = await quizApiService.updateQuestion(id, updatedQuestion)
        const index = questions.findIndex(q => q.id === id)
        questions.splice(index, 1, response.data)
      } catch (error) {
        console.error(error)
      }
    }

    async function deleteQuestion(id) {
      // delete the question with the specified ID
      try {
        await quizApiService.deleteQuestion(id)
        const index = questions.findIndex(q => q.id === id)
        questions.splice(index, 1)
      } catch (error) {
        console.error(error)
      }
    }

    return {
      questions,
      loading,
      fetchQuestions,
      addQuestion,
      editQuestion,
      deleteQuestion,
      showQuestion
    }
  }
}
</script>
