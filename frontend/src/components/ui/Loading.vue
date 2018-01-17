<template>
  <div id="container" v-show="isShow">
    <div id="container_wrap">
      <div id="section_list_4" class="section_tab_contents clearfix">
        <div class="loading_wrap">
          <div class="title">{{ titleText }}</div>
          <div class="prologue">{{ descriptionText }}</div>
          <div class="loading_chart">
            <div id="loading"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//레이아웃 호출
export default {
  name: 'Loading',

  props: {
    isShow: {
      type: Boolean,
      default () {
        return false
      }
    },
    titleText: {
      type: String,
      default () {
        return '타겟을 최적화 하는 중입니다.'
      }
    },
    descriptionText: {
      type: String,
      default () {
        return '조금만 기다려 주시면, 계정에 적합한 기본 타겟이 생성됩니다.'
      }
    }
  },

  data () {
    return {
    }
  }
}
</script>

<style lang="css" scoped>
</style>
