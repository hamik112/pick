<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
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
            <div class="contents_title">사용픽셀</div>
            <ui-select :selectData="adAccountPixels" data-key="adAccountPixels" :onClick="selectOnClick"></ui-select>
          </div>
          <div class="use_date">
            <div>수집기간 : 최근</div>
            <div><input type="text" v-model="registrationDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="registrationName"></div>
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
      <button class="next_btn" @click="createRegistration()">타겟 만들기</button>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'

export default {
  name: '',

  components: {
    'ui-select': Select
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
    }
  },

  data () {
    return {
      registrationDay: '30',
      registrationName: '',

      subSelect:false,
      subInput:false,

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
        name: this.registrationName,
        retention_days: this.registrationDay,

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
          alert('회원가입 타겟 생성 실패')
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
