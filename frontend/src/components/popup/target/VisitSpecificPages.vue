<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
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
            <div class="contents_title">사용픽셀</div>
            <ui-select :selectData="adAccountPixels" data-key="adAccountPixels" :onClick="selectOnClick"></ui-select>
          </div>
          <div class="use_date">
            <div>수집기간 : 최근</div>
            <div><input type="text" v-model="visitSpecificPagesDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="visitSpecificPagesName"></div>
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
              <div class="account_title">"아래 그룹로 유입된 사람"중</div>
              <div>
                <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subSelect">
                <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subInput">
                <input type="text" v-if="subInput"><span>일</span>
              </div>
            </div>
            <div class="generate_url_list">
              <div v-for="(item, index) in fields" class="url_list clearfix">
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
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createVisitSpecificPages()" v-if="makeType == 'add'">타겟 만들기</button>
      <button class="next_btn" @click="createVisitSpecificPages()" v-if="makeType == 'modify'">수정</button>
      <button class="delete_btn" v-if="makeType == 'modify'">삭제</button>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
  name: 'VisitSpecificPages',

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
      visitSpecificPagesDay: '30',
      visitSpecificPagesName: '',

      subSelect:false,
      subInput:false,

      dialogShow:false,
      dialogData:{
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },
      nextStage:false,

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
      },

      fields: [
        {
          "url": '',
          "number": 0,
          "key": 0,
          "select": {
            emptyText: '전체URL',
            textList: [
              '전체URL',
              '부분URL'
            ]
          }
        }
      ]

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

      if(mode == 'visiteSiteSpecific') {
        this.createVisiteSpecificPagesNext()
      }

      //모드별 동작
      this.nextStage = true
      this.dialogShow = false;
    },
    dialogCancel() {
      this.nextStage = false;
      this.dialogShow = false;
    },

    selectOnClick(item) {
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

    multiSelectOnClick(item, index) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      this.fields[key].select.emptyText = item
    },

    fieldBtn (item, type) {
      let index = 0
      if(type === 'add') {
        index++
        let obj = {
          "url": '',
          "number": index,
          "key": index,
          "select": {
            emptyText: '전체URL',
            textList: [
              '전체URL',
              '부분URL'
            ]
          }
        }
        this.fields.push(obj)
      }else{
        index--
        this.fields.splice(this.fields.indexOf(item), 1)
      }
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
      } else {
        //컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('입력한 내용으로 타겟을 생성하겠습니까?', 'confirm', 'visiteSiteSpecific')
      }
    },
    createVisiteSpecificPagesNext() {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'visit_specific_pages',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.visitSpecificPagesName,
        retention_days: this.visitSpecificPagesDay,

        detail: this.findSelectKey('selectUser'),
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
