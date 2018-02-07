<template>
  <div id="container" v-show="isShow">
    <div id="container_wrap">
      <div id="section_list_4" class="clearfix">
        <div class="Useless_wrap">
          <div class="title">{{ titleText }}</div>
          <div class="prologue">{{ descriptionText }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//레이아웃 호출
export default {
  name: 'Useless',

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
        return '다른 광고 계정을 선택해 주세요'
      }
    },
    descriptionText: {
      type: String,
      default () {
        return '해당 광고 계정은 픽셀을 보유하고 있지 않거나 사용이 불가능합니다.'
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
