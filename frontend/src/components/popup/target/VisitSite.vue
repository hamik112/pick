<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
    </transition>
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_01.png" alt="neo"></div>
          <div class="title_info">
            <p>사이트 방문</p>
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
            <div><input type="text" v-model="collectionPeriod" onkeyup="this.value=this.value.replace(/[^0-9]/g, '')"><span>일</span></div>
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
              <div class="account_title">"사이트 방문자"중</div>
              <div>
                <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subSelect">
                <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subInput">
                <input type="text" v-if="subInput" v-model="unvisitedPeriod" onkeyup="this.value=this.value.replace(/[^0-9]/g, '')"><span>일</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createVisitSite()" v-if="makeType == 'add'">타겟 만들기</button>
      <button class="next_btn" @click="updateVisitSite()" v-if="makeType == 'modify'">수정</button>
      <button class="delete_btn" @click="createVisitSiteDelete()" v-if="makeType == 'modify'">삭제</button>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'VisitSite',

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
    },
    makeItem: {
      type: Object
    }
  },

  mounted () {
    console.log('mounted', this.makeItem)
    if (this.makeType === 'modify') {
      this.collectionPeriod = numberFormatter(this.makeItem.description.retention_days)
      this.targetName = this.makeItem.name
      this.audienceSize = numberFormatter(this.makeItem.display_count)
    }
  },

  data () {
    return {
      collectionPeriod: '30',
      unvisitedPeriod: '1',
      targetName: '',
      audienceSize: '-',

      subSelect: false,
      subInput: false,

      dialogShow:false,
      dialogData:{
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },
      nextStay:false,

      selectUser: {
        emptyText: '전체 고객',
        textList: [
          '전체 고객',
          '이용 시간 상위 고객', // 셀렉트박스 표시 (5/15/25 %)
          '특정일 동안 미방문 고객', // 숫자 입력 텍스트필드 표시
          '구매고객',
          '미 구매고객',
          '장바구니 이용 고객',
          '전환완료 고객',
          '미 전환 고객',
          '회원가입 고객'
        ],
        keyList: [
          'total',
          'usage_time_top', // 셀렉트박스 표시 (5/15/25 %)
          'non_visit', // 숫자 입력 텍스트필드 표시
          'purchase',
          'non_purchase',
          'add_to_cart',
          'conversion',
          'non_conversion',
          'registration'
        ],
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

  watch: {
    collectionPeriod (day) {
      if (day > 180) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('수집 기간은 최대 180일까지만 가능합니다.', 'alert')
        this.collectionPeriod = 180
      } else if (this.collectionPeriod === '0') {
        alert('수집 기간은 최소 1일입니다.')
        this.collectionPeriod = 1
      }
    },

    unvisitedPeriod (day) {
      if(day >= this.collectionPeriod) {
        alert('미방문 기간은 수집 기간보다 작아야합니다.')
        this.unvisitedPeriod = this.collectionPeriod - 1
      }
    },

    targetName (name) {
      if (name.length > 48) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('타겟 이름은 최대 48자까지만 가능합니다.', 'alert')
        this.targetName = name.substr(0,48)
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

      if (mode === 'visitSite') {
        this.createVisitSiteNext()
      } else if (mode === 'visitSiteDelete') {
        this.$emit('deleteCustomTarget', this.makeItem.id)
      } else if (mode === 'visitSiteUpdate') {
        this.updateVisitSiteNext()
      }

      //모드별 동작
      this.nextStay = true
      this.dialogShow = false;
    },
    dialogCancel() {
      this.nextStay = false;
      this.dialogShow = false;
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

    createVisitSite () {
      if (this.collectionPeriod.length === 0) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('수집 기간을 입력해주세요.', 'alert')
      } else if (this.unvisitedPeriod.length === 0) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('미방문 기간을 입력해주세요.', 'alert')
      } else if (this.targetName.length === 0) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('타겟 이름을 입력해주세요.', 'alert')
      } else {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('입력한 내용으로 타겟을 생성하겠습니까?', 'confirm', 'visitSite')
      }
    },

    createVisitSiteNext () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'visit_site',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.targetName,
        retention_days: this.collectionPeriod,

        detail: this.findSelectKey('selectUser'),
        input_percent: this.findSelectKey('selectSub')
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
          this.dialogOpen('사이트방문 타겟 생성 실패', 'alert')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    },

    createVisitSiteDelete () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'visitSiteDelete')
    },

    updateVisitSite () {
      this.dialogOpen('수정하시겠습니까?', 'confirm', 'visitSiteUpdate')
    },

    updateVisitSiteNext () {
      console.log('update call')
      let params = {
        pickdata_account_target_id: this.makeItem.id,
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'visit_site',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.targetName,
        retention_days: this.collectionPeriod,

        detail: this.findSelectKey('selectUser'),
        input_percent: this.findSelectKey('selectSub')
      }

      this.$http.put('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          this.dialogOpen('사이트방문 타겟 수정 실패', 'alert')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target delete: ', err)
      })
    },

    // TODO Delete Function
    createVisiteSiteDeleteNext () {
      console.log('delete call')

      // this.$http.put('/pickdata_account_target/custom_target', {
      //   pickdata_account_target_id: this.makeItem.id
      // })
      // .then((response) => {
      //   console.log(response)
      // })
      // .catch(err => {
      //   this.$emit('close')
      //   console.log('/pickdata_account_target/custom_target delete: ', err)
      // })\\
      this.$http.delete('/pickdata_account_target/custom_target', {
        data: {
          pickdata_account_target_id: this.makeItem.id
        }
      })
      .then((response) => {
        const success = response.data.success
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
          this.dialogOpen('사이트방문 타겟 삭제 실패', 'alert')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target delete: ', err)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
