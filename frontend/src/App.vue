<template>
  <div id="vue_wrap">
    <Header v-show="isHeader"></Header>
    <Aside v-show="isAside"></Aside>
    <router-view></router-view>
    <Footer v-show="isFooter"></Footer>
  </div>
</template>

<script>
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import Aside from '@/components/layout/Aside'

export default {
  name: 'app',

  components: {
    'Header': Header,
    'Footer': Footer,
    'Aside': Aside
  },

  data () {
    return {
      isHeader: false,
      isAside: false,
      isFooter: false
    }
  },

  watch: {
    '$route' (to, from) {
      this.showLayout(to.name)
    }
  },

  created () {
    this.showLayout(this.$router.currentRoute.name)
  },

  methods: {
    showLayout (name) {
      if (name === 'Intro') {
        this.isHeader = false
        this.isAside = false
        this.isFooter = false
      } else {
        this.isHeader = true
        this.isAside = true
        this.isFooter = true
      }
    }
  }
}
</script>

<style lang="scss">
	@import 'assets/sass/main.scss'
</style>
