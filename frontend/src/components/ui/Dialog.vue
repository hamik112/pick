<template>
  <div class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container dialog-widget">
        <div class="check_alert">
          <div class="alert_top">
            <p>{{ dialogData.emptyText }}</p>
          </div>
          <div class="alert_bottom" v-if="dialogData.type == 'confirm'">
            <button class="alert_complete confirm" @click="onConfirm">확인</button>
            <button class="alert_close cancel" @click="onCancel">취소</button>
          </div>
          <div class="alert_bottom" v-if="dialogData.type == 'alert'">
            <button class="confirm alert_complete complete_v2" @click="onCancel">확인</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {

  name: 'Dialog',
  props:{
    dialogData: {
      type:Object,
      default () {
        return {
          emptyText:'',
          type:'',
          mode:''
        }
      }
    }
  },
  data () {
    return {

    }
  },
  methods: {
    onConfirm() {
      this.$emit("ok");
    },
    onCancel() {
      this.$emit("cancel");
    }
  }
}
</script>

<style lang="css" scoped>
.dialog-widget { background-color:#fff;  }
</style>