<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
    </transition>
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_08.png" alt="neo"></div>
          <div class="title_info">
            <p>단계별 전환</p>
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
            <div><input type="text" v-model="coversionDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="coversionName"></div>
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
              <div class="account_title">전환 관련 속성 선택</div>
              <div>
                <ui-select :selectData="this.selectConversionUser" data-key="selectConversionUser" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="value_input_wrap" v-if="subConversionInput">
                <input type="text">
                <p>단계 완료 후 이탈 고객</p>
              </div>
            </div>
            <div class="generate_url_list">
              <div class="url_list clearfix">
                <div class="url_text clearfix">
                  <p>해당 단계 완료 URL</p>
                </div>
                <div class="url_input">
                  <input type="text">
                </div>
              </div>
              <div class="url_list clearfix">
                <div class="url_text clearfix">
                  <p>다음 단계 완료 URL</p>
                </div>
                <div class="url_input">
                  <input type="text">
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="btn_wrap">
          <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
          <button class="next_btn" @click="createConversion()" v-if="makeType == 'add'">타겟 만들기</button>
          <button class="next_btn" @click="createConversion()" v-if="makeType == 'modify'">수정</button>
          <button class="delete_btn" @click="createConversionDelete()" v-if="makeType == 'modify'">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'Conversion',

  components: {
    'ui-select': Select,
    'ui-dialog': Dialog
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
    },
    makeItem: {
      type: Object
    }
  },

  data () {
    return {
      coversionDay: '30',
      coversionName: '',

      subConversionInput: false,

      dialogShow: false,
      dialogData: {
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },

      selectConversionUser: {
        emptyText: '미 전환 고객',
        textList: [
          '미 전환 고객',
          '전환 1단계 완료 고객',
          '전환 2단계 완료 고객',
          '전환 3단계 완료 고객',
          '전환 4단계 완료 고객',
          '전환 5단계 완료 고객',
          '특정 단계 완료(URL)'//단계완료 이탈 입력박스
        ]
      }
    }
  },

  methods: {
    dialogOpen (emptyText, type, mode) {
      this.dialogData['emptyText'] = emptyText
      this.dialogData['type'] = type
      this.dialogData['mode'] = mode
      this.dialogShow = true;
    },

    dialogOk () {
      const mode = this.dialogData.mode

      if(mode == 'conversion') {
        this.createVisitSpecificPagesNext()
      } else if (mode === 'conversionDelete') {
        this.$emit('deleteCustomTarget', this.makeItem.id)
      }

      //모드별 동작
      this.nextStage = true
      this.dialogShow = false;
    },

    dialogCancel () {
      this.nextStage = false;
      this.dialogShow = false;
    },

    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")

      this.subConversionInput = false

      if(textCheck === '특정단계완료(URL)'){
        this.subConversionInput = true
      }
      this[key].emptyText = item
    },

    findSelectKey (selectName) {
      /*
      Select Key 가져오기
      */
      const emptyText = this[selectName].emptyText
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return keyList[textList.indexOf(emptyText)]
    },

    createConversion () {
      console.log('TODO createConversion')
      // let params = {
      //   fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
      //   target_type: 'visit_site',
      //   pixel_id: this.findSelectKey('adAccountPixels'),
      //   name: this.visitSiteName,
      //   retention_days: this.visitSiteDay,
      //
      //   detail: this.findSelectKey('selectUser'),
      //   input_percent: this.findSelectKey('selectSub')
      // }
      //
      // this.$http.post('/pickdata_account_target/custom_target', params)
      // .then((response) => {
      //   var success = response.data.success
      //   if (success == "YES") {
      //     // success
      //     this.$eventBus.$emit('getAccountTarget')
      //   } else {
      //     alert('사이트방문 타겟 생성 실패')
      //     throw('success: ' + success)
      //   }
      //   this.$emit('close')
      // })
      // .catch(err => {
      //   this.$emit('close')
      //   console.log('/pickdata_account_target/custom_target: ', err)
      // })
    },

    createConversionDelete () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'conversionDelete')
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
