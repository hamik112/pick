import Vue from 'vue'
import Router from 'vue-router'
import Intro from '@/components/Intro'
// Page Import
import TargetPick from '@/components/pages/TargetPick'
import TargetReport from '@/components/pages/TargetReport'
import CreativeLibrary from '@/components/pages/CreativeLibrary'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Intro',
      component: Intro
    },
    {
      path: '/pick',
      name: 'TargetPick',
      component: TargetPick
    },
    {
      path: '/report',
      name: 'TargetReport',
      component: TargetReport
    },
    {
      path: '/library',
      name: 'CreativeLibrary',
      component: CreativeLibrary
    }
  ]
})
