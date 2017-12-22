import Vue from 'vue'
import Router from 'vue-router'
import Intro from '@/components/Intro'
import Main from '@/components/Main'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Intro',
      component: Intro
    },
    {
      path: '/main',
      name: 'Main',
      component: Main
    }
  ]
})
