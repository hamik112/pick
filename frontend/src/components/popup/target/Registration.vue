<template>
  <div class="target_contents_wrap clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
    </transition>
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_07.png" alt="member"></div>
          <div class="title_info">
            <p>회원가입</p>
            <p>타겟의 속성을 정의하세요</p>
          </div>
        </div>
        <div class="use_wrap">
          <div class="use_select">
            <div class="contents_title">사용 픽셀</div>
            <ui-select :selectData="adAccountPixels" data-key="adAccountPixels" :onClick="selectOnClick"></ui-select>
          </div>
          <div class="use_date">
            <div>수집 기간 : 최근</div>
            <div><input type="text" v-model="collectionPeriod"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟 이름</div>
          <div><input type="text" v-model="targetName"></div>
        </div>
        <div class="target_data">
          <div class="contents_title">타겟 모수</div>
          <div>
            <span>{{ this.audienceSize }}</span>명
          </div>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <div class="target_generate">
            <div class="account_info">
              <div class="account_title">"회원가입한 사람" 중</div>
              <div>
                <ui-select :selectData="this.selectRegistrationUser" data-key="selectRegistrationUser" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subSelect">
                <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subInput">
                <input type="text" v-if="subInput"><span>일</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createRegistration()" v-if="makeType == 'add'">타겟 만들기</button>
      <button class="delete_btn" @click="createRegistrationDelete()" v-if="makeType == 'modify'">삭제</button>
      <button class="next_btn" @click="updateRegistration()" v-if="makeType == 'modify'">타겟 수정하기</button>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'Registration',

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

  created () {
    this.$eventBus.$on('modifyRegistrationTarget', this.modifyRegistrationTarget)
  },

  beforeDestroy () {
    this.$eventBus.$off('modifyRegistrationTarget', this.modifyRegistrationTarget)
  },

  data () {
    return {
      collectionPeriod: '30',
      targetName: '',
      audienceSize: '-',

      subSelect:false,
      subInput:false,

      dialogShow:false,
      dialogData:{
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },
      nextStage:false,

      selectRegistrationUser: {
        emptyText: '전체 고객',
        textList: [
          '전체 고객',
          '이용 시간 상위 고객', // 셀렉트박스 표시 (5/15/25 %)
          '미 구매 고객',
          '전환 완료 고객',
          '미 전환 고객'
        ],
        keyList: [
          'total',
          'usage_time_top',
          'non_purchase',
          'conversion',
          'non_conversion'
        ]
      },
      selectSub: {
        emptyText: '5%',
        textList: [
          '5%',
          '15%',
          '25%'
        ],
        keyList: [
          '5',
          '15',
          '25'
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

      if(mode == 'registration') {
        // TODO
      } else if (mode === 'registrationDelete') {
        this.$emit('deleteCustomTarget', this.makeItem.id)
      } else if (mode === 'registrationUpdate') {
        this.updateRegistrationNext()
      }

      //모드별 동작
      this.nextStage = true
      this.dialogShow = false
    },

    dialogCancel() {
      this.nextStage = false
      this.dialogShow = false
    },

    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")
      this.subSelect = false
      this.subInput = false

      //서브 입력창 체크
      if(textCheck === '이용시간상위고객' || key === 'selectSub') {
        this.subSelect = true
      }else if(textCheck === '특정일동안미방문고객') {
        this.subInput = true
      }
      this[key].emptyText = item
    },

    findSelectText (selectName, key) {
      /*
      Select Text 가져오기
      */
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return textList[keyList.indexOf(key)]
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

    createRegistration () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'registration',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.targetName,
        retention_days: this.collectionPeriod,

        detail: this.findSelectKey('selectRegistrationUser'),
        input_percent: this.findSelectKey('selectSub')
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success;
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
          this.dialogOpen('회원가입 타겟 생성 실패', 'alert')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    },

    createRegistrationDelete () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'registrationDelete')
    },

    updateRegistration () {
      this.dialogOpen('수정하시겠습니까?', 'confirm', 'registrationUpdate')
    },

    updateRegistrationNext () {
      console.log('update call')
      let params = {
        pickdata_account_target_id: this.makeItem.id,
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'registration',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.targetName,
        retention_days: this.collectionPeriod,

        detail: this.findSelectKey('selectRegistrationUser'),
        input_percent: this.findSelectKey('selectSub')
      }

      this.$http.put('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          this.dialogOpen('회원가입 타겟 생성 실패', 'alert')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target delete: ', err)
      })
    },

    // /fb_ad_accounts/ad_account_pixels call after
    modifyRegistrationTarget () {
      console.log('modifyVisitSiteTarget')

      // Custom Target인 경우 params가 존재
      if(this.makeItem.description.params) {
        const params = this.makeItem.description.params
        const detail = params.detail

        // 사용 픽셀
        this.adAccountPixels.emptyText = this.findSelectText('adAccountPixels', this.makeItem.description.params.pixel_id)

        // 수집 기간
        this.collectionPeriod = numberFormatter(this.makeItem.description.retention_days)

        // 타겟 이름
        this.targetName = this.makeItem.name

        // 타겟 모수
        this.audienceSize = numberFormatter(this.makeItem.display_count)

        // 회원가입한 사람중 @
        if (detail === 'total') {
          // 전체 고객
          this.selectRegistrationUser.emptyText = '전체 고객'
        } else if (detail === 'usage_time_top') {
          // 이용 시간 상위 고객
          this.selectRegistrationUser.emptyText = '이용 시간 상위 고객'
          this.selectSub.emptyText = params.input_percent + '%'
          this.subSelect = true
        } else if (detail === 'non_purchase') {
          // 미구매 고객
          this.selectRegistrationUser.emptyText = '미구매 고객'
        } else if (detail === 'conversions') {
          // 전환 완료 고객
          this.selectRegistrationUser.emptyText = '전완 완료 고객'
        } else if (detail === 'non_conversion') {
          // 미전환 고객
          this.selectRegistrationUser.emptyText = '미전환 고객'
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
