import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuizPage from '../views/QuizPage.vue'
import AdminPage from '../views/AdminPage.vue'
import QuestionPage from '../views/QuestionPage.vue'
import AddQuestion from '../views/AddQuestion.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/quiz-page',
      name: 'QuizPage',
      component: QuizPage
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: AdminPage
    },
    {
      path: '/questions/:id',
      name: 'QuestionPage',
      component: QuestionPage,
      props : true
    },
    {
      path: '/addQuestion',
      name: 'addQuestion',
      component: AddQuestion
    },
  ]
})

export default router
