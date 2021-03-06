import Vue from 'vue'
import Router from 'vue-router'
import Intro from '@/components/Intro'

// Page Import
import TargetPick from '@/components/pages/TargetPick'
import TargetReport from '@/components/pages/TargetReport'
import CreativeLibrary from '@/components/pages/CreativeLibrary'
import Setting from '@/components/pages/Setting'
import { requireAuth } from '../utils/auth'

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
      beforeEnter: requireAuth,
      name: 'TargetPick',
      component: TargetPick
    },
    {
      path: '/report',
      beforeEnter: requireAuth,
      name: 'TargetReport',
      component: TargetReport
    },
    {
      path: '/library',
      beforeEnter: requireAuth,
      name: 'CreativeLibrary',
      component: CreativeLibrary
    },
    {
      path: '/setting',
      beforeEnter: requireAuth,
      name: 'Setting',
      component: Setting
    }
  ]
})
