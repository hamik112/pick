<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_04.png" alt="neo"></div>
          <div class="title_info">
            <p>구글애널리틱스</p>
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
            <div><input type="text" v-model="utmTargetDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="utmTargetName"></div>
        </div>
        <div class="target_data">
          <div class="contents_title">타겟 모수</div>
          <div>
            <span>12,000</span>명
          </div>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody google_body clearfix">
          <div class="target_generate google_analytics">
            <div class="account_info">
              <div class="account_title">"아래 UTM 속성으로 유입된 사람" 중</div>
              <div>
                <div class="select_btn">
                  <div class="select_contents">
                    <ui-select :selectData="this.selectUser" data-key="selectUser" :onClick="selectOnClick"></ui-select>
                  </div>
                </div>
              </div>
              <div class="account_date" v-if="subSelect">
                <ui-select :selectData="this.selectSub" data-key="selectSub" :onClick="selectOnClick"></ui-select>
              </div>
              <div class="account_date" v-if="subInput">
                <input type="text" v-if="subInput"><span>일</span>
              </div>
            </div>
            <div class="generate_url_list">
              <form id="google_url_form" class="url_list clearfix" v-on:submit.prevent="addAnalyData">
                <div class="url_select clearfix">
                  <div class="select_btn">
                    <div class="select_contents">
                      <ui-select id="utm_key" :selectData="this.selectUtmType" data-key="selectUtmType" :onClick="selectOnClick"></ui-select>
                    </div>
                  </div>
                </div>
                <div class="url_input">
                  <input id="utm_name" type="text" v-model="inputUtmName" placeholder="값 입력 후 엔터를 치면 아래에 입력됩니다.">
                </div>
              </form>
            </div>
          </div>
        </div>
        <div class="analytics_tab_wrap">
          <div class="analytics_tab_widget clearfix">
            <ul class="clearfix">
              <li @click="wTabs(0,'wTab')" v-bind:class="[(wTab.tab1 === true) ? 'active' : '']">source</li>
              <li @click="wTabs(1,'wTab')" v-bind:class="[(wTab.tab2 === true) ? 'active' : '']">medium</li>
              <li @click="wTabs(2,'wTab')" v-bind:class="[(wTab.tab3 === true) ? 'active' : '']">campaign</li>
              <li @click="wTabs(3,'wTab')" v-bind:class="[(wTab.tab4 === true) ? 'active' : '']">team</li>
              <li @click="wTabs(4,'wTab')" v-bind:class="[(wTab.tab5 === true) ? 'active' : '']">content</li>
              <li @click="wTabs(5,'wTab')" v-bind:class="[(wTab.tab6 === true) ? 'active' : '']">custom</li>
            </ul>
          </div>
          <div class="analytics_tab_list">
            <div id="tab_list_1" class="analytics_tab_contents clearfix" v-if="wTab.tab1">
              <ul>
                <li v-for="(item,index) in gAddData.utm_source" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_source')"><img src="../../../assets/images/target/target_list_close.png" alt=""></span></li>
              </ul>
              <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_source')"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button></div>
            </div>
            <div id="tab_list_2" class="analytics_tab_contents clearfix" v-if="wTab.tab2">
              <ul>
                <li v-for="(item,index) in gAddData.utm_medium" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_medium')"><img src="../../../assets/images/target/target_list_close.png" alt=""></span></li>
              </ul>
              <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_meidum')"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button></div>
            </div>
            <div id="tab_list_3" class="analytics_tab_contents clearfix" v-if="wTab.tab3">
              <ul>
                <li v-for="(item,index) in gAddData.utm_campaign" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_campaign')"><img src="../../../assets/images/target/target_list_close.png" alt=""></span></li>
              </ul>
              <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_campaign')"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button></div>
            </div>
            <div id="tab_list_4" class="analytics_tab_contents clearfix" v-if="wTab.tab4">
              <ul>
                <li v-for="(item,index) in gAddData.utm_term" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_term')"><img src="../../../assets/images/target/target_list_close.png" alt=""></span></li>
              </ul>
              <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_term')"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button></div>
            </div>
            <div id="tab_list_5" class="analytics_tab_contents clearfix" v-if="wTab.tab5">
              <ul>
                <li v-for="(item,index) in gAddData.utm_content" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_content')"><img src="../../../assets/images/target/target_list_close.png" alt=""></span></li>
              </ul>
              <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_content')"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button></div>
            </div>
            <div id="tab_list_6" class="analytics_tab_contents clearfix" v-if="wTab.tab6">
              <ul>
                <li v-for="(item,index) in gAddData.utm_custom" class="sticker_btn"><span>{{ item.name }}</span><span class="close-btn" @click="deleteAnalyData(item,'utm_custom')"><img src="../../../assets/images/target/target_list_close.png" alt=""></span></li>
              </ul>
              <div class="list_close_btn"><button type="button" @click="deleteAnalyData('all','utm_custom')"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button></div>
            </div>
          </div>
        </div>
        <div class="btn_wrap">
          <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
          <button class="next_btn" @click="createUtmTarget()">타겟 만들기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'

export default {
  name: 'UtmTarget',

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
      utmTargetDay: '30',
      utmTargetName: '',
      inputUtmName: '',

      subSelect:false,
      subInput:false,

      gAddData: {
        utm_source: [],
        utm_medium: [],
        utm_campaign: [],
        utm_term: [],
        utm_content: [],
        utm_custom: []
      },

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
      selectUtmType: {
        emptyText: 'utm_source',
        textList: [
          'utm_source',
          'utm_medium',
          'utm_campaign',
          'utm_term',
          'utm_content',
          'utm_custom'
        ]
      },
      wTab: {
        tab1: true,
        tab2: false,
        tab3: false,
        tab4: false,
        tab5: false,
        tab6: false
      }
    }
  },

  methods: {
    wTabs (num, obj) {
      const tabs = Object.keys(this[obj])
      for(let i = 0; i < tabs.length; i++) {
        if(num == i) {
          this.wTab[tabs[i]] = true
        }else{
          this.wTab[tabs[i]] = false
        }
      }
    },

    addAnalyData() {
      const elId = event.target.id
      const utmKey = document.getElementById('utm_key').getElementsByClassName('select')[0].innerText.replace(/\s/gi, "")
      const utmName = document.getElementById('utm_name').value
      const gData = this.gAddData[utmKey]
      const keyData = this.selectUtmType.textList
      const newData = {
        number: gData.length + 1,
        name: utmName
      }
      //선택필드 탭 활성화
      for(let i = 0; i < keyData.length; i++) {
        if(keyData[i] === utmKey) {
          this.wTabs(i, 'wTab')
          break
        }
      }
      //동일 이름 체크
      for(let i = 0; i < gData.length; i++) {
        if(gData[i].name === utmName) {
          alert('같은 UTM값이 존재합니다.')
          break
          this.inputUtmName = ''
          return false
        }
      }
      gData.push(newData)
      this.inputUtmName = ''

      return false
    },

    deleteAnalyData(item, key){
      const elId = event.target.closest('.analytics_tab_contents').id
      const addListEl = document.getElementById(elId)
      const addlistLi = addListEl.getElementsByTagName('li')

      if(item === 'all') {
        this.gAddData[key].splice(0, addlistLi.length)
      }else{
        this.gAddData[key].splice(this.gAddData[key].indexOf(item), 1)
      }
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

    findSelectKey (selectName) {
      /*
      Select Key 가져오기
      */
      const emptyText = this[selectName].emptyText
      const textList = this[selectName].textList
      const keyList = this[selectName].keyList
      return keyList[textList.indexOf(emptyText)]
    },

    convertUtmName (data) {
      let result = []
      data.forEach(function (item, index) {
        result.push(item['name'])
      })
      return result
    },

    createUtmTarget () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'utm_target',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.utmTargetName,
        retention_days: this.utmTargetDay,

        detail: this.findSelectKey('selectUser'),
        input_percent: this.findSelectKey('selectSub'),

        sources: this.convertUtmName(this.gAddData.utm_source),
        mediums: this.convertUtmName(this.gAddData.utm_medium),
        campaigns: this.convertUtmName(this.gAddData.utm_campaign),
        terms: this.convertUtmName(this.gAddData.utm_term),
        contents: this.convertUtmName(this.gAddData.utm_content),
        customs: this.convertUtmName(this.gAddData.utm_custom)
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          alert('구글애널리틱스 타겟 생성 실패')
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
