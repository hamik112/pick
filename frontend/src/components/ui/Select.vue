<template>
  <div class="select_btn">
    <div class="select_contents">
      <div class="select" v-on:click="onShow"><p>{{ selectData.emptyText }}</p></div>
      <ul class="select_view" :style="this.selectViewStyle">
        <li v-for="item in selectData.textList">{{ item }}</li>
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
      }
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
      required: false
    }
  },

  methods: {
    onShow: function () {
      if (this.selectViewStyle.display === 'none') {
        this.selectViewStyle.display = 'block'
      } else {
        this.selectViewStyle.display = 'none'
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
