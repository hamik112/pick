<template>
  <div class="select_btn">
    <div class="select_contents" tabindex="-1" @blur="hide">
      <div class="select" v-on:click="onShow"><p v-bind:class="this.pArrowUp">{{ selectData.emptyText }}</p></div>
      <ul class="select_view" :style="this.selectViewStyle" v-click-outside="hide">
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
    emptyText: {
      type: String,
      default () {
        return '선택 하세요'
      }
    },
    selectData: {
      type: Object,
      default () {
        return {
          emptyText: 'Select..',
          textList: [
            'Select1',
            'Select2',
            'Select3'
          ]
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
      this.selectViewStyle.display = 'none'
    }
  }
}
</script>

<style lang="css" scoped>
</style>
