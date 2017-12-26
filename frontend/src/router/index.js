import Vue from 'vue'
import Router from 'vue-router'
import Intro from '@/components/Intro'
import Main from '@/components/Main'
//Page Import
import TargetPick from '@/components/pages/TargetPick'
import TargetReport from '@/components/pages/TargetReport'
import CreativeLibrary from '@/components/pages/CreativeLibrary'

Vue.use(Router)

const routes = routeFrame();

function routeFrame() {
  //ROUTING GRUP
  let routesArray = []

  let paths = ['/','/Main','/TargetPick','/TargetReport','/CreativeLibrary'] //URL
  let names = ['Intro','Main','TargetPick','TargetReport','CreativeLibrary'] //PAGE NAME
  let components = [Intro,Main,TargetPick,TargetReport,CreativeLibrary] //COMPONENTS NAME


  for(var i = 0; i < components.length; i++) {
    var routeObj = {
      path: paths[i],
      name: names[i],
      component: components[i]
    }
    routesArray.push(routeObj)
  }
  return routesArray;
}

//라우팅 정보
export const router = new Router({
  routes:routes
})

export default router
