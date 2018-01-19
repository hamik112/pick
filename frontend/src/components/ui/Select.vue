<template>
  <div class="select_btn">
    <div class="select_contents" tabindex="-1" @blur="hide">
      <div class="select" v-on:click="onShow"><p v-bind:class="this.pArrowUp">{{ selectData.emptyText }}</p></div>
      <ul class="select_view" :style="this.selectViewStyle">
        <li v-for="item in selectData.textList" @click="onClick(item)" v-on:click="onShow">{{ item }}</li>
      </ul>
    </div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      selectViewStyle: {
        display: 'none'
      },
      pArrowUp: ''
    }
  },

  props: {
    selectData: {
      type: Object,
      default () {
        return {
          emptyText: '픽셀 이벤트가 없습니다.',
          textList: []
        }
      }
    },
    onClick: {
      type: Function,
      required: false,
      default: function (item) {
        console.log('default', item)
      }
    }
  },
  methods: {
    onShow: function () {
      if (this.selectViewStyle.display === 'none') {
        this.pArrowUp = 'arrow_up'
        this.selectViewStyle.display = 'block'
      } else {
        this.pArrowUp = ''
        this.selectViewStyle.display = 'none'
      }
    },
    hide:function() {
      this.pArrowUp = ''
      this.selectViewStyle.display = 'none'
    }
  }
}
</script>

<style lang="css" scoped>
</style>
