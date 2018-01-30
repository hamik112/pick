<template>
  <div class="target_contents_wrap clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if="dialogShow" @ok="dialogOk()" @cancel="dialogCancel()"></ui-dialog>
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
            <span>{{ this.audienceSize }}</span>
            <span v-show="isNumber">명</span>
          </div>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <div class="target_generate">
            <div class="account_info">
              <div class="account_title">"회원가입한 사람" 중</div>
              <div>
                <ui-select :selectData="this.selectCustomer" data-key="selectCustomer" :onClick="selectOnClick"></ui-select>
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
    <div v-if="makeType === 'modify'" class="modify_prologue">* 설정 수정시 기존 생성된 타겟과 병합되어 모수가 중복될 수 있습니다. 특별한 상황이 아니면 설정의 수정을 지양해주세요.</div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="makeType === 'modify' ? $emit('close') : tabMove(0)">취소</button>
      <button class="next_btn" @click="createRegistrationTarget()" v-if="makeType === 'add'">타겟 만들기</button>
      <button class="delete_btn" @click="deleteRegistrationTarget()" v-if="makeType === 'modify'">삭제</button>
      <button class="next_btn" @click="updateRegistrationTarget()" v-if="makeType === 'modify'">타겟 수정하기</button>
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
          textList: [ '불러오는 중 입니다.' ]
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
      isNumber: false,

      subSelect: false,
      subInput: false,

      dialogShow: false,
      dialogData: {
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },
      nextStage:false,

      selectCustomer: {
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
    dialogOpen (emptyText, type, mode) {
      this.dialogData['emptyText'] = emptyText
      this.dialogData['type'] = type
      this.dialogData['mode'] = mode
      this.dialogShow = true;
    },

    // 다이얼로그 확인 클릭시
    dialogOk () {
      const mode = this.dialogData.mode

      if(mode === 'createRegistrationTarget') {
        // Create Target -----------------------------------------------------------------
        let params = {
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'registration',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,

          detail: this.findSelectKey('selectCustomer'),
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

      } else if (mode === 'deleteRegistrationTarget') {
        // Delete Target -----------------------------------------------------------------
        this.$emit('deleteCustomTarget', this.makeItem.id)

      } else if (mode === 'updateRegistrationTarget') {
        // Update Target -----------------------------------------------------------------
        let params = {
          pickdata_account_target_id: this.makeItem.id,
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'registration',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,

          detail: this.findSelectKey('selectCustomer'),
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
      }

      // 모드별 동작
      this.nextStage = true
      this.dialogShow = false
    },

    // 다이얼로그 취소 클릭시
    dialogCancel () {
      this.nextStage = false
      this.dialogShow = false
    },

    selectOnClick (item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")
      this.subSelect = false
      this.subInput = false

      // 서브 입력창 체크
      if(textCheck === '이용시간상위고객' || key === 'selectSub') {
        this.subSelect = true
      }else if(textCheck === '특정일동안미방문고객') {
        this.subInput = true
      }
      this[key].emptyText = item
    },

    findSelectText (selectName, key) {
      // Select Text 가져오기
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return textList[keyList.indexOf(key)]
    },

    findSelectKey (selectName) {
      // Select Key 가져오기
      const emptyText = this[selectName].emptyText
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return keyList[textList.indexOf(emptyText)]
    },

    // Create Target Dialog
    createRegistrationTarget () {
      this.dialogOpen('입력한 내용으로 타겟을 생성하시겠습니까?', 'confirm', 'createRegistrationTarget')
    },

    // Delete Target Dialog
    deleteRegistrationTarget () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'deleteRegistrationTarget')
    },

    // Update Target Dialog
    updateRegistrationTarget () {
      this.dialogOpen('수정하시겠습니까?', 'confirm', 'updateRegistrationTarget')
    },

    // 수정 클릭시 타겟 생성 팝업 데이터 초기화 (/fb_ad_accounts/ad_account_pixels call after)
    modifyRegistrationTarget () {
      const description = this.makeItem.description
      const params = description.params
      const detail = params.detail

      // 사용 픽셀
      this.adAccountPixels.emptyText = this.findSelectText('adAccountPixels', params.pixel_id)

      // 수집 기간
      this.collectionPeriod = numberFormatter(description.retention_days)

      // 타겟 이름
      this.targetName = this.makeItem.name

      // 타겟 모수
      const displayCount = this.makeItem.display_count

      if (displayCount === '규모가 적음') {
        this.audienceSize = displayCount
        this.isNumber = false
      } else if (displayCount === '생성중') {
        this.audienceSize = displayCount
        this.isNumber = false
      } else {
        this.audienceSize = numberFormatter(this.makeItem.display_count)
        this.isNumber = true
      }

      // 회원가입한 사람중 @
      if (detail === 'total') {
        // 전체 고객
        this.selectCustomer.emptyText = '전체 고객'
      } else if (detail === 'usage_time_top') {
        // 이용 시간 상위 고객
        this.selectCustomer.emptyText = '이용 시간 상위 고객'
        this.selectSub.emptyText = params.input_percent + '%'
        this.subSelect = true
      } else if (detail === 'non_purchase') {
        // 미구매 고객
        this.selectCustomer.emptyText = '미구매 고객'
      } else if (detail === 'conversions') {
        // 전환 완료 고객
        this.selectCustomer.emptyText = '전완 완료 고객'
      } else if (detail === 'non_conversion') {
        // 미전환 고객
        this.selectCustomer.emptyText = '미전환 고객'
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
