<template>
  <div class="target_contents_wrap clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if="dialogShow" @ok='dialogOk()' @cancel="dialogCancel()"></ui-dialog>
    </transition>
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_02.png" alt="neo"></div>
          <div class="title_info">
            <p>특정페이지 방문</p>
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
        <div class="target_inner_tbody particula_inner clearfix">
          <div class="target_generate">
            <div class="account_info">
              <div class="account_title">"아래 URL을 방문한 사람" 중</div>
              <div>
                <ui-select :selectData="selectCustomer" data-key="selectCustomer" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subSelect">
                <ui-select :selectData="selectSub" data-key="selectSub" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subInput">
                <input type="text" v-if="subInput" v-model="unvisitedPeriod"><span>일</span>
              </div>
            </div>
            <div class="generate_url_list">
              <div v-for="(item, index) in fields" :key="index" class="url_list clearfix">
                <div class="url_select clearfix">
                  <ui-select :selectData="item.select" :data-key="index" :onClick="multiSelectOnClick"></ui-select>
                </div>
                <div class="url_input">
                  <input type="text" v-model="item.url">
                </div>
                <div class="url_btn clearfix">
                  <div class="add"><button type="button" @click="fieldBtn(item, 'add')">+</button></div>
                  <div class="del" v-if="index > 0"><button type="button" @click="fieldBtn(item, 'del')">-</button></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="makeType === 'modify'" class="modify_prologue">* 설정 수정시 기존 생성된 타겟과 병합되어 모수가 중복될 수 있습니다. 특별한 상황이 아니면 설정의 수정을 지양해주세요.</div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="makeType === 'modify' ? $emit('close') : tabMove(0)">취소</button>
      <button class="next_btn" @click="createVisitSpecificPages()" v-if="makeType === 'add'">타겟 만들기</button>
      <button class="delete_btn" @click="deleteVisitSpecificPages()" v-if="makeType === 'modify'">삭제</button>
      <button class="next_btn" @click="updateVisitSpecificPages()" v-if="makeType === 'modify'">타겟 수정하기</button>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'VisitSpecificPages',

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
    this.$eventBus.$on('modifyVisitSepcificPagesTarget', this.modifyVisitSepcificPagesTarget)
  },

  beforeDestroy () {
    this.$eventBus.$off('modifyVisitSepcificPagesTarget', this.modifyVisitSepcificPagesTarget)
  },

  data () {
    return {
      collectionPeriod: 30,
      unvisitedPeriod: 0,
      targetName: '',
      audienceSize: '-',
      isNumber: false,

      subSelect:false,
      subInput:false,

      dialogShow:false,
      dialogData:{
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
          '특정일 동안 미방문 고객', // 숫자 입력 텍스트필드 표시
          '구매고객',
          '미구매 고객',
          '장바구니 이용 고객',
          '전환완료 고객',
          '미전환 고객',
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
        textList: [ '5%', '15%', '25%' ],
        keyList: [ '5', '15', '25' ]
      },

      fields: [
        {
          "url": '',
          "number": 0,
          "key": 0,
          "select": {
            emptyText: '전체URL',
            textList: [ '전체URL', '부분URL' ]
          }
        }
      ]
    }
  },

  watch: {
    collectionPeriod (day) {
      if (day > 180) {
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

    // 다이얼로그 확인 클릭시
    dialogOk() {
      const mode = this.dialogData.mode

      if(mode == 'visitSpecificPages') {
        // Create Target -----------------------------------------------------------------
        let params = {
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'visit_specific_pages',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,
          exclusion_retention_days: this.unvisitedPeriod,

          detail: this.findSelectKey('selectCustomer'),
          input_percent: this.findSelectKey('selectSub')
        }

        const urlParams = this.findVisitSpecificPagesParam()
        params['eq_list'] = urlParams['eqList']
        params['contain_list'] = urlParams['containList']

        this.$http.post('/pickdata_account_target/custom_target', params)
        .then((response) => {
          var success = response.data.success
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
            this.dialogOpen('특정페이지 방문 타겟 생성 실패', 'alert')
            throw('success: ' + success)
          }
          this.$emit('close')
        })
        .catch(err => {
          this.$emit('close')
          console.log('/pickdata_account_target/custom_target: ', err)
        })

      } else if (mode === 'deleteVisitSpecificPages') {
        // Delete Target -----------------------------------------------------------------
        this.$emit('deleteCustomTarget', this.makeItem.id)

      } else if (mode === 'updateVisitSpecificPages') {
        // Update Target -----------------------------------------------------------------
        let body = {
          pickdata_account_target_id: this.makeItem.id,
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'visit_specific_pages',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,
          exclusion_retention_days: this.unvisitedPeriod,

          detail: this.findSelectKey('selectCustomer'),
          input_percent: this.findSelectKey('selectSub')
        }

        const urlParams = this.findVisitSpecificPagesParam()
        body['eq_list'] = urlParams['eqList']
        body['contain_list'] = urlParams['containList']

        this.$http.put('/pickdata_account_target/custom_target', body)
        .then((response) => {
          var success = response.data.success
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            this.dialogOpen('특정페이지방문 타겟 수정 실패', 'alert')
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
      this.dialogShow = false;
    },

    // 다이얼로그 취소 클릭시
    dialogCancel() {
      this.nextStage = false;
      this.dialogShow = false;
    },

    selectOnClick(item) {
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

    multiSelectOnClick(item, index) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      this.fields[key].select.emptyText = item
    },

    fieldBtn (item, type) {
      let index = 0
      if (type === 'add') {
        index++
        let obj = {
          "url": '',
          "number": index,
          "key": index,
          "select": {
            emptyText: '전체URL',
            textList: [ '전체URL', '부분URL' ]
          }
        }
        this.fields.push(obj)
      } else {
        index--
        this.fields.splice(this.fields.indexOf(item), 1)
      }
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

    findVisitSpecificPagesParam () {
      const data = this.fields
      let eqList = []
      let containList = []
      data.forEach(function (item, index) {
        if (item.select.emptyText === '전체URL') {
          eqList.push(item.url)
        } else if (item.select.emptyText === '부분URL') {
          containList.push(item.url)
        }
      })
      return {
        eqList: eqList,
        containList: containList
      }
    },

    // Create Target Dialog
    createVisitSpecificPages () {
      // URL 목록
      let fieldUrls = []
      this.fields.forEach(field => {
        fieldUrls.push(field.url)
      })

      // URL이 모두 입력 되었는지 확인
      let validation = fieldUrls.every(fieldUrl => {
        // 빈 URL이 없다면 true 반환
        return fieldUrl !== ''
      })

      if (validation === false) {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('입력되지 않은 URL이 있습니다.', 'alert')
      } else if (this.collectionPeriod.length === 0) {
        this.dialogOpen('수집 기간을 입력해주세요.', 'alert')
      } else if (this.unvisitedPeriod.length === 0) {
        this.dialogOpen('미방문 기간을 입력해주세요.', 'alert')
      } else if (this.targetName.length === 0) {
        this.dialogOpen('타겟 이름을 입력해주세요.', 'alert')
      } else {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('입력한 내용으로 타겟을 생성하겠습니까?', 'confirm', 'visitSpecificPages')
      }
    },

    // Delete Target Dialog
    deleteVisitSpecificPages () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'deleteVisitSpecificPages')
    },

    // Update Target Dialog
    updateVisitSpecificPages () {
      // URL 목록
      let fieldUrls = []
      this.fields.forEach(field => {
        fieldUrls.push(field.url)
      })

      // URL이 모두 입력 되었는지 확인
      let validation = fieldUrls.every(fieldUrl => {
        // 빈 URL이 없다면 true 반환
        return fieldUrl !== ''
      })

      if (validation === false) {
        this.dialogOpen('입력되지 않은 URL이 있습니다.', 'alert')
      } else if (this.collectionPeriod.length === 0) {
        this.dialogOpen('수집 기간을 입력해주세요.', 'alert')
      } else if (this.unvisitedPeriod.length === 0) {
        this.dialogOpen('미방문 기간을 입력해주세요.', 'alert')
      } else if (this.targetName.length === 0) {
        this.dialogOpen('타겟 이름을 입력해주세요.', 'alert')
      } else {
        this.dialogOpen('수정하시겠습니까?', 'confirm', 'updateVisitSpecificPages')
      }
    },

    // 수정 클릭시 타겟 생성 팝업 데이터 초기화 (/fb_ad_accounts/ad_account_pixels call after)
    modifyVisitSepcificPagesTarget () {
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

      // 아래 URL을 방문한 사람중 @
      if (detail === 'total') {
        // 전체 고객
        this.selectCustomer.emptyText = '전체 고객'
      } else if (detail === 'usage_time_top') {
        // 이용 시간 상위 고객
        this.selectCustomer.emptyText = '이용 시간 상위 고객'
        this.selectSub.emptyText = params.input_percent + '%'
        this.subSelect = true
      } else if (detail === 'non_visit') {
        // 특정일 동안 미방문 고객
        this.selectCustomer.emptyText = '특정일 동안 미방문 고객'
        this.subInput = true
      } else if (detail === 'purchase') {
        // 구매 고객
        this.selectCustomer.emptyText = '구매고객'
      } else if (detail === 'non_purchase') {
        // 미구매 고객
        this.selectCustomer.emptyText = '미구매 고객'
      } else if (detail === 'add_to_cart') {
        // 장바구니 이용 고객
        this.selectCustomer.emptyText = '장바구니 이용 고객'
      } else if (detail === 'conversion') {
        // 전환완료 고객
        this.selectCustomer.emptyText = '전환완료 고객'
      } else if (detail === 'non_conversion') {
        // 미전환 고객
        this.selectCustomer.emptyText = '미전환 고객'
      } else if (detail === 'registration') {
        // 회원가입 고객
        this.selectCustomer.emptyText = '회원가입 고객'
      } else {
        console.log('nothing..', detail)
      }

      this.fields = []
      let index = 0

      // 전체URL
      if(this.makeItem.description.params.eq_list) {
        this.makeItem.description.params.eq_list.forEach(url => {
          let field = {
            "url": url,
            "number": index,
            "key": index,
            "select": {
              emptyText: '전체URL',
              textList: [ '전체URL', '부분URL' ]
            }
          }

          index++
          this.fields.push(field)
        })
      }

      // 부분URL
      if(this.makeItem.description.params.contain_list) {
        this.makeItem.description.params.contain_list.forEach(url => {
          let field = {
            "url": url,
            "number": index,
            "key": index,
            "select": {
              emptyText: '부분URL',
              textList: [ '전체URL', '부분URL' ]
            }
          }

          index++
          this.fields.push(field)
        })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
