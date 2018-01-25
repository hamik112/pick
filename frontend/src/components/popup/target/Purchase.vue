<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
    </transition>
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_05.png" alt="buy"></div>
          <div class="title_info">
            <p>구매</p>
            <p>타겟의 속성을 정의하세요</p>
          </div>
        </div>
        <div class="use_wrap">
          <div class="use_select">
            <div class="contents_title">사용픽셀</div>
            <ui-select :selectData="adAccountPixels" data-key="adAccountPixels" :onClick="selectOnClick"></ui-select>
          </div>
          <div class="use_date">
            <div>수집기간 : 최근</div>
            <div><input type="text" v-model="purchaseDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="purchaseName"></div>
        </div>
        <div class="target_data">
          <div class="contents_title">타겟 모수</div>
          <div>
            <span>12,000</span>명
          </div>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <div class="target_generate">
            <div class="account_info">
              <div class="account_title">"구매한 사람" 중</div>
              <div>
                <ui-select :selectData="this.selectPurchaseUser" data-key="selectPurchaseUser" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subInputPurchaseCount">
                <input type="text" v-model="purchaseCount"><span>회</span>
              </div>
              <div class="account_date" v-if="subInputPurchaseAmount">
                <input type="text" v-model="purchaseAmount"><span>원</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createPurchase()" v-if="makeType == 'add'">타겟 만들기</button>
      <button class="next_btn" @click="createPurchase()" v-if="makeType == 'modify'">수정</button>
      <button class="delete_btn">삭제</button>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'Purchase',

  components: {
    'ui-select': Select,
    'ui-dialog':Dialog
  },

  props: {
    isShow: {
      type: Boolean,
      default () {
        return false
      }
    },
    adAccountPixels: {
      type: Object,
      default () {
        return {
          emptyText: '불러오는 중 입니다.',
          textList: [
            '불러오는 중 입니다.'
          ]
        }
      }
    },
    tabMove: {
      type: Function
    },
    makeType: {
      type:String
    }
  },

  data () {
    return {
      purchaseDay: '30',
      purchaseName: '',
      purchaseCount: '0',
      purchaseAmount: '0',

      subInputPurchaseCount: false,
      subInputPurchaseAmount: false,

      dialogShow:false,
      dialogData:{
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },
      nextStage:false,

      selectPurchaseUser: {
        emptyText: '전체 고객',
        textList: [
          '전체 고객',
          '특정 구매횟수 이상 구매 고객', // 셀렉트박스 표시 (5/15/25 %)
          '특정 구매금액 이상 구매 고객', // 숫자 입력 텍스트필드 표시
        ],
        keyList: [
          'total',
          'purchase_count',
          'purchase_amount'
        ]
      }
    }
  },

  methods: {
    dialogOpen(emptyText, type, mode) {
      this.dialogData['emptyText'] = emptyText
      this.dialogData['type'] = type
      this.dialogData['mode'] = mode
      this.dialogShow = true;
    },
    dialogOk() {
      const mode = this.dialogData.mode

      //모드별 동작
      this.nextStage = true
      this.dialogShow = false;
    },
    dialogCancel() {
      this.nextStage = false;
      this.dialogShow = false;
    },


    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")

      this.subInputPurchaseCount = false
      this.subInputPurchaseAmount = false

      //서브 입력창 체크
      if (textCheck === '특정구매횟수이상구매고객') {
        this.subInputPurchaseCount = true
      } else if (textCheck === '특정구매금액이상구매고객') {
        this.subInputPurchaseAmount = true
      }
      this[key].emptyText = item
    },

    findSelectKey (selectName) {
      /*
      Select Key 가져오기
      */
      console.log('selectName', selectName, this[selectName])
      const emptyText = this[selectName].emptyText
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return keyList[textList.indexOf(emptyText)]
    },

    createPurchase () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'purchase',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.purchaseName,
        retention_days: this.purchaseDay,

        detail: this.findSelectKey('selectPurchaseUser'),
        purchase_count: this.purchaseCount,
        purchase_amount: this.purchaseAmount
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
          this.dialogOpen('구매 타겟 생성 실패', 'alert')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
