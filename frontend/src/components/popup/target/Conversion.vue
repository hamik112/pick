<template>
  <div class="target_contents_wrap clearfix" v-if="isShow">
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
              <div class="account_title">전환 관련 속성 선택</div>
              <div>
                <ui-select :selectData="this.selectConversionUser" data-key="selectConversionUser" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="value_input_wrap" v-if="subConversionInput">
                <input type="text" v-model="conversionSubText">
                <p>단계 완료 후 이탈 고객</p>
              </div>
            </div>
            <div class="generate_url_list" v-if="subConversionInput">
              <div class="url_list clearfix">
                <div class="url_text clearfix">
                  <p>해당 단계 완료 URL</p>
                </div>
                <div class="url_input">
                  <input type="text" v-model="conversionCompleteUrl">
                </div>
              </div>
              <div class="url_list clearfix">
                <div class="url_text clearfix">
                  <p>다음 단계 완료 URL</p>
                </div>
                <div class="url_input">
                  <input type="text" v-model="conversionNextCompleteUrl">
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="makeType === 'modify'" class="modify_prologue">* 설정 수정시 기존 생성된 타겟과 병합되어 모수가 중복될 수 있습니다. 특별한 상황이 아니면 설정의 수정을 지양해주세요.</div>
        <div class="btn_wrap">
          <button class="before_btn close_pop" @click="makeType === 'modify' ? $emit('close') : tabMove(0)">취소</button>
          <button class="next_btn" @click="createConversionTarget()" v-if="makeType == 'add'">타겟 만들기</button>
          <button class="delete_btn" @click="deleteConversionTarget()" v-if="makeType == 'modify'">삭제</button>
          <button class="next_btn" @click="updateConversionTarget()" v-if="makeType == 'modify'">타겟 수정하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
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

  created () {
    this.$eventBus.$on('modifyConversionTarget', this.modifyConversionTarget)
  },

  beforeDestroy () {
    this.$eventBus.$off('modifyConversionTarget', this.modifyConversionTarget)
  },

  data () {
    return {
      collectionPeriod: '30',
      targetName: '',
      audienceSize: '-',
      isNumber: false,

      conversionSubText: '',
      conversionCompleteUrl: '',
      conversionNextCompleteUrl: '',

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
        ],
        keyList: [
          'non_conversion',
          'conversion 1step',
          'conversion 2step',
          'conversion 3step',
          'conversion 4step',
          'conversion 5step',
          'conversion url'
        ]
      }
    }
  },

  watch: {
    collectionPeriod (day) {
      if (day > 180) {
        // 컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('수집 기간은 최대 180일까지만 가능합니다.', 'alert')
        this.collectionPeriod = 180
      } else if (this.collectionPeriod === '0') {
        alert('수집 기간은 최소 1일입니다.')
        this.collectionPeriod = 1
      }
    },

    targetName (name) {
      if (name.length > 48) {
        // 컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('타겟 이름은 최대 48자까지만 가능합니다.', 'alert')
        this.targetName = name.substr(0,48)
      }
    },

    conversionSubText (name) {
      if (name.length > 8) {
        // 컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('최대 8자까지만 가능합니다.', 'alert')
        this.conversionSubText = name.substr(0,8)
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

    // 다이얼로그 확인 클릭시
    dialogOk () {
      const mode = this.dialogData.mode

      if (mode === 'createConversion') {
        // Create Target -----------------------------------------------------------------
        let params = {
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'conversion',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,

          detail: this.findSelectKey('selectConversionUser')
        }
        if (this.findSelectKey('selectConversionUser') == 'conversion url') {
          params['step_name'] = this.conversionSubText
          params['current_complete_url'] = this.conversionCompleteUrl
          params['next_complete_url'] = this.conversionNextCompleteUrl
        }

        this.$http.post('/pickdata_account_target/custom_target', params)
        .then((response) => {
          var success = response.data.success
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
            this.dialogOpen('단계별 전환 타겟 생성 실패', 'alert')
            throw('success: ' + success)
          }
          this.$emit('close')
        })
        .catch(err => {
          this.$emit('close')
          console.log('/pickdata_account_target/custom_target: ', err)
        })


      } else if (mode === 'deleteConversion') {
        // Delete Target -----------------------------------------------------------------
        this.$emit('deleteCustomTarget', this.makeItem.id)


      } else if (mode === 'updateConversion') {
        // Update Target -----------------------------------------------------------------
        let params = {
          pickdata_account_target_id: this.makeItem.id,
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'conversion',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,

          detail: this.findSelectKey('selectConversionUser')
        }
        if (this.findSelectKey('selectConversionUser') == 'conversion url') {
          params['step_name'] = this.conversionSubText
          params['current_complete_url'] = this.conversionCompleteUrl
          params['next_complete_url'] = this.conversionNextCompleteUrl
        }

        this.$http.put('/pickdata_account_target/custom_target', params)
        .then((response) => {
          var success = response.data.success
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            this.dialogOpen('단계별 전환 타겟 수정 실패', 'alert')
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
      this.nextStay = true
      this.dialogShow = false
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

    findSelectText (selectName, key) {
      // Select Text 가져오기
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

    // Create Target Dialog
    createConversionTarget () {
      if (this.collectionPeriod.length === 0) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('수집 기간을 입력해주세요.', 'alert')
      } else if (this.targetName.length === 0) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('타겟 이름을 입력해주세요.', 'alert')
      } else {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('입력한 내용으로 타겟을 생성하시겠습니까?', 'confirm', 'createConversion')
      }
    },

    // Delete Target Dialog
    deleteConversionTarget () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'deleteConversion')
    },

    // Update Target Dialog
    updateConversionTarget () {
      if (this.collectionPeriod.length === 0) {
        this.dialogOpen('수집 기간을 입력해주세요.', 'alert')
      } else if (this.targetName.length === 0) {
        this.dialogOpen('타겟 이름을 입력해주세요.', 'alert')
      } else {
        this.dialogOpen('수정하시겠습니까?', 'confirm', 'updateConversion')
      }
    },

    modifyConversionTarget () {
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

      // 사이트 방문자중 @
      if (detail === 'non_conversion') {
        // 미 전환 고객
        this.selectConversionUser.emptyText = '미 전환 고객'
      } else if (detail === 'conversion 1step') {
        // 전환 1단계 완료 고객
        this.selectConversionUser.emptyText = '전환 1단계 완료 고객'
      } else if (detail === 'conversion 2step') {
        // 전환 2단계 완료 고객
        this.selectConversionUser.emptyText = '전환 2단계 완료 고객'
      } else if (detail === 'conversion 3step') {
        // 전환 3단계 완료 고객
        this.selectConversionUser.emptyText = '전환 3단계 완료 고객'
      } else if (detail === 'conversion 4step') {
        // 전환 4단계 완료 고객
        this.selectConversionUser.emptyText = '전환 4단계 완료 고객'
      } else if (detail === 'conversion 5step') {
        // 전환 5단계 완료 고객
        this.selectConversionUser.emptyText = '전환 5단계 완료 고객'
      } else if (detail === 'conversion url') {
        // 특정 단계 완료(URL)
        this.selectConversionUser.emptyText = '특정 단계 완료(URL)'
        this.subConversionInput = true
        this.conversionSubText = params.step_name
        this.conversionCompleteUrl = params.current_complete_url
        this.conversionNextCompleteUrl = params.next_complete_url
      } else {
        console.log('nothing..', detail)
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
