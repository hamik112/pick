// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import store from './store'
import App from './App'
import router from './router'
import axios from 'axios'
import qs from 'qs'

Vue.prototype.$http = axios
Vue.prototype.$eventBus = new Vue()
Vue.prototype.$qs = qs

Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  store,
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
