<template>
  <div class="select_btn">
    <div class="select_contents" tabindex="-1" @blur="hide">
      <div class="select" v-on:click="onShow"><p v-bind:class="this.pArrowUp">{{ selectData.selectedPixelEvent }}</p></div>
      <ul class="select_view" :style="this.selectViewStyle">
        <li v-for="pixelEvent in selectData.pixelEvents" :key="pixelEvent" @click="onClick(pixelEvent)" v-on:click="onShow">{{ pixelEvent }}</li>
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
          selectedPixelEvent: '픽셀 이벤트가 없습니다.',
          pixelEvents: []
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
