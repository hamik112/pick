<template>
  <div class="modal-mask">
    <div class="modal-wrapper">
      <div class="modal-container">
        <div class="layer-pop-widget">
          <div class="popup-widget" id="target_pop_01">
            <div class="popup-contents clearfix">
              <div class="pop_title_wrap">
                <div class="pop_title">타겟 만들기 (<span id="page-number">1</span>/2)</div>
                <p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
              </div>

              <!-- 카테고리 선택 탭 -->
              <div class="pop_tab_wrap clearfix" v-if="tabAction.tabActive1.show">
                <div class="cate_contents_widget">
                  <ul class="target_pick_01">
                    <li @click="tabMove(1)">
                      <span>사이트방문</span>
                    </li>
                    <li @click="tabMove(2)">
                      <span>특정페이지 방문</span>
                    </li>
                    <li @click="tabMove(3)">
                      <span>NEO 타겟</span>
                    </li>
                    <li @click="tabMove(4)">
                      <span>구글애널리틱스</span>
                    </li>
                  </ul>
                  <ul class="target_pick_02">
                    <li @click="tabMove(5)">
                      <span>구매</span>
                    </li>
                    <li @click="tabMove(6)">
                      <span>장바구니</span>
                    </li>
                    <li @click="tabMove(7)">
                      <span>회원가입</span>
                    </li>
                    <li @click="tabMove(8)">
                      <span>단계별 전환</span>
                    </li>
                  </ul>
                </div>
                <div class="btn_wrap">
                  <button type="button" class="close_pop" @click="$emit('close')">취소</button>
                </div>
              </div>

              <!-- 사이트 방문 탭 -->
              <visit-site
                :isShow="tabAction.tabActive2.show"
                :adAccountPixels="this.adAccountPixels"
                :tabMove="tabMove"
                @close="$emit('close')"></visit-site>

              <!-- 특정 페이지 방문 탭 -->
              <visit-specific-pages
                :isShow="tabAction.tabActive3.show"
                :adAccountPixels="this.adAccountPixels"
                :tabMove="tabMove"
                @close="$emit('close')"></visit-specific-pages>

              <!-- 네오 탭 -->
              <neo-target
                :isShow="tabAction.tabActive4.show"
                :adAccountPixels="this.adAccountPixels"
                :tabMove="tabMove"
                @close="$emit('close')"></neo-target>

        <!-- 구글애널리틱스 탭 -->
        <utm-target
          :isShow="tabAction.tabActive5.show"
          :adAccountPixels="this.adAccountPixels"
          :tabMove="tabMove"
          @close="$emit('close')"></utm-target>

        <!-- 구매 탭 -->
        <purchase
          :isShow="tabAction.tabActive6.show"
          :adAccountPixels="this.adAccountPixels"
          :tabMove="tabMove"
          @close="$emit('close')"></purchase>

        <!-- 장바구니 탭 -->
        <add-to-cart
          :isShow="tabAction.tabActive7.show"
          :adAccountPixels="this.adAccountPixels"
          :tabMove="tabMove"
          @close="$emit('close')"></add-to-cart>



        <!-- 회원가입 탭 -->
        <registration
          :isShow="tabAction.tabActive8.show"
          :adAccountPixels="this.adAccountPixels"
          :tabMove="tabMove"
          @close="$emit('close')"></registration>

        

        <!-- 단계별 전환 -->
        <div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive9.show">
          <div class="target_contents_inner">
            <div class="target_thead">
              <div class="main_title">
                <div><img src="../../assets/images/target/target_logo_08.png" alt="neo"></div>
                <div class="title_info">
                  <p>단계별 전환</p>
                  <p>타겟의 속성을 정의하세요</p>
                </div>
              </div>
              <div class="use_wrap">
                <div class="use_select">
                  <div class="contents_title">사용픽셀</div>
                  <ui-select :selectData="this.adAccountPixels" data-key="adAccountPixels" :onClick="selectTarget"></ui-select>
                </div>
                <div class="use_date">
                  <div>수집기간 : 최근</div>
                  <div><input type="text"><span>일</span></div>
                </div>
              </div>
              <div class="target_name">
                <div class="contents_title">타겟이름</div>
                <div><input type="text"></div>
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
                      <ui-select :selectData="this.selectUser4" data-key="selectUser4" :onClick="selectTarget"></ui-select>
                    </div>
                    <div class="value_input_wrap" v-if="subInput4">
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
                <button class="next_btn">타겟 만들기</button>
              </div>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>
</div>
</div>
</div>

</template>

<script>

import { numberFormatter } from '@/components/utils/Formatter'
// UI
import Select from '@/components/ui/Select'
import VisitSite from '@/components/popup/target/VisitSite'
import VisitSpecificPages from '@/components/popup/target/VisitSpecificPages'
import NeoTarget from '@/components/popup/target/NeoTarget'
import UtmTarget from '@/components/popup/target/UtmTarget'
import Purchase from '@/components/popup/target/Purchase'
import AddToCart from '@/components/popup/target/AddToCart'
import Registration from '@/components/popup/target/Registration'

export default {
  name: 'TargetMake01',
  components:{
    'ui-select': Select,
    'visit-site': VisitSite,
    'visit-specific-pages': VisitSpecificPages,
    'neo-target': NeoTarget,
    'utm-target': UtmTarget,
    'purchase': Purchase,
    'add-to-cart': AddToCart,
    'registration': Registration
  },
  mounted() {
    let emptyText = ''
    let textList = []
    let keyList = []

    this.$http.get('/fb_ad_accounts/ad_account_pixels', {
      params: {
        'fb_ad_account_id': localStorage.getItem('fb_ad_account_id')
      }
    })
    .then(res => {
      const response = res.data
      const data = response.data
      const success = response.success
      if (success === 'YES') {
        data.forEach(function(item, index) {
          textList.push(item.name)
          keyList.push(item.id)
          if (index === 0) {
            emptyText = item.name
          }
        })

        this.adAccountPixels.emptyText = emptyText
        this.adAccountPixels.textList = textList
        this.adAccountPixels.keyList = keyList
      } else {
        console.log('/fb_ad_accounts/ad_account_pixels fail')
      }
    })



  },
  data () {
    return {
      visitSiteDay: '30',
      visitSiteName: '',

      visitSpecificPagesDay: '30',
      visitSpecificPagesName: '',

      neoTargetDay: '30',
      neoTargetName: '',
      neoTargetType: 'media',

      utmTargetDay: '30',
      utmTargetName: '',
      inputUtmName: '',

      purchaseDay: '30',
      purchaseName: '',
      purchaseCount: '0',
      purchaseAmount: '0',

      addToCartDay: '30',
      addToCartName: '',

      registrationDay: '30',
      registrationName: '',

      subSelect:false,
      subInput:false,
      subInput2:false,
      subInput3:false,
      subInput4:false,

      tabAction:{
        tabActive1:{
          show:true
        },
        tabActive2:{
          show:false
        },
        tabActive3:{
          show:false
        },
        tabActive4:{
          show:false
        },
        tabActive5:{
          show:false
        },
        tabActive6:{
          show:false
        },
        tabActive7:{
          show:false
        },
        tabActive8:{
          show:false
        },
        tabActive9:{
          show:false
        }
      },

      categoryName:'',

      //싱글 셀렉트
      adAccountPixels: {
        emptyText: '불러오는 중 입니다.',
        textList: [
          '불러오는 중 입니다.'
        ]
      },
      //사이트방문\
      //특정페이지
      //네오
      neoAccounts: [],
      neoCampaigns: [],
      neoKeywords: [],
      selectedNeoAccounts: [],
      selectedNeoCampaigns: [],
      selectedNeoKeywords: [],
      checkDataNeoAccounts: [],
      checkDataNeoCampaigns: [],
      checkDataNeoKeywords: [],
      addNeoAccounts:[],
      addNeoCampaigns:[],
      addNeoKeywords:[],

      select9: {
        emptyText: '특정일 동안 미방문 고객',
        textList: [
          '이벤트1',
          '이벤트2',
          '이벤트3'
        ]
      },
      //구글
      selectAddToCartUser: {
        emptyText: '전체 고객',
        textList: [
          '전체 고객',
          '미 구매 고객'
        ],
        keyList: [
          'total',
          'non_purchase'
        ]
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
      selectUser2: {
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
      },
      selectUser3: {
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
      selectUser4: {
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
      select12: {
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
      //구매
      //장바구니
      //회원가입
      //단계별 전환

      //sample
      advs:[
        { "number": "1", "name": "LF몰", "campaign":"페이스북1", "count":"3,716", "type_id":"13" },
        { "number": "2", "name": "LF몰2", "campaign":"페이스북2", "count":"3,716", "type_id":"11" },
        { "number": "3", "name": "LF몰3", "campaign":"페이스북3", "count":"3,716", "type_id":"15" },
        { "number": "4", "name": "LF몰4", "campaign":"페이스북4", "count":"3,716", "type_id":"17" }
      ],

      addAdvs:[],
      checkData:[],
      selected:[],

      //tabs
      wTab:{
        tab1:true,
        tab2:false,
        tab3:false,
        tab4:false,
        tab5:false,
        tab6:false
      },
      //analytics sample
      gData:{
        utm_source:[
          { number:1, name:"naver" },
          { number:2, name:"daum" },
          { number:3, name:"google" }
        ],
        utm_medium:[],
        utm_compaign:[],
        utm_term:[],
        utm_content:[],
        utm_custom:[],
      },

      //analytics add sample
      gAddData:{
        utm_source:[],
        utm_medium:[],
        utm_campaign:[],
        utm_term:[],
        utm_content:[],
        utm_custom:[]
      },

      fields:[
        //sample
        {
          "url": '',
          "number":0,
          "key":0,
          "select":{
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
    //페이지 방문 추가 삭제
    fieldBtn(item,type) {
      let index = 0
      if(type === 'add') {
        index++
        let obj = {
          "url": '',
          "number":index,
          "key":index,
          "select":{
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
    //타겟만들기 카테고리 탭
    tabMove(activeNumber, beforeNumber) {
      let tabArray = ['tabActive1','tabActive2','tabActive3','tabActive4','tabActive5','tabActive6','tabActive7','tabActive8','tabActive9']
      let pageNum = (activeNumber == 0) ? '1':'2'

      document.getElementById('page-number').innerText = pageNum

      for(let i = 0; i < tabArray.length; i++) {
        if(i == activeNumber) {
          this.tabAction[tabArray[i]].show = true
        }else{
          this.tabAction[tabArray[i]].show = false
        }
      }
      //리셋 데이터
      //공용 서브 탭 초기화
      this.wTab = {
        tab1:true,
        tab2:false,
        tab3:false,
        tab4:false,
        tab5:false,
        tab6:false
      },
      //서브 셀렉터 초기화
      this.subSelect = false
      this.subInput = false
      this.subInput2 = false
      this.subInput3 = false
    },
    //서브 공용 탭
    wTabs(num,obj) {
      const tabs = Object.keys(this[obj])
      for(let i = 0; i < tabs.length; i++) {
        if(num == i) {
          this.wTab[tabs[i]] = true
        }else{
          this.wTab[tabs[i]] = false
        }
      }
    },
    //개별 셀렉팅
    selectTarget(item) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      const textCheck = item.replace(/\s/gi, "")
      this.subSelect = false
      this.subInput = false
      this.subInput2 = false
      this.subInput3 = false
      this.subInput4 = false
      //서브 입력창 체크
      if(textCheck === '이용시간상위고객' || key === 'selectSub') {
        this.subSelect = true
      }else if(textCheck === '특정일동안미방문고객') {
        this.subInput = true
      }else if(textCheck === '특정구매횟수이상구매고객') {
        this.subInput2 = true
      }else if(textCheck === '특정구매금액이상구매고객') {
        this.subInput3 = true
      }else if(textCheck === '특정단계완료(URL)'){
        this.subInput4 = true
      }
      this[key].emptyText = item
    },
    //멀티 셀렉팅
    multiSelect(item, index) {
      const key = event.target.closest('.select_btn').getAttribute('data-key')
      this.fields[key].select.emptyText = item
    },

    //매체 삭제
    deleteAddAdvs(item) {
      const checkAdd = this.addAdvs
      const addListEl = document.getElementById('adv-list-2')
      const addlistLi = addListEl.getElementsByTagName('li')
      if(item === 'all') {
        for(let i = 0; i < addlistLi.length; i++) {
          this.advs.push(checkAdd[i])
        }
        this.addAdvs.splice(0, addlistLi.length)
      }else{
        this.addAdvs.splice(this.addAdvs.indexOf(item), 1)
        this.advs.push(item)
      }
    },

    //구글애널리틱스 매체 추가
    addAnalyData() {
      const elId = event.target.id
      const utmKey = document.getElementById('utm_key').getElementsByClassName('select')[0].innerText.replace(/\s/gi, "")
      const utmName = document.getElementById('utm_name').value
      const gData = this.gAddData[utmKey]
      const keyData = this.select12.textList
      const newData = {
        number:gData.length + 1,
        name:utmName
      }
      //선택필드 탭 활성화
      for(let i = 0; i < keyData.length; i++) {
        if(keyData[i] === utmKey) {
          this.wTabs(i,'wTab')
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
    //구글애널리틱스 매체삭제
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

    //전체선택
    allCheck(value,key1,key2,before,after) {
      const me = this
      var selected = []
      if (value) {
        this.checkFilter(key1)
        me[key1].forEach(function (item) {
          selected.push(item.number)
        });
      }
      me[key2] = selected;
    },
    //체크리스트 추가
    checkList (before,after) {

      const me = this

      this.checkFilter(before)

      me[after] = me[after].concat(me.checkData)
      me.checkData.forEach(function(value, index) {
        me[before] = me[before].filter(function(item) {
          return item !== value
        })
      })

      this.selected = []
      me.checkData = []
    },

    //체크 중복 필터
    checkFilter(type) {
      let elId = "adv-list-1"
      let ul = document.getElementById(elId)
      let items = ul.getElementsByTagName("li")
      let itemsData = this[type]

      for (let i = 0; i < items.length; i++) {
        let checkBox = items[i].getElementsByTagName('input')[0].checked
        if(checkBox == true) {
          let checkItemsId = items[i].getElementsByTagName('input')[0].getAttribute('data-id')
          for(let idx = 0; idx < itemsData.length; idx++) {
            if(checkItemsId == itemsData[idx]['type_id']) {
              this.checkData.push(itemsData[idx])
            }
          }
        }
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

    findSelectedNeoKey (listName, key) {
      let result = []
      const data = this[listName]
      data.forEach(function (item, index) {
        result.push(item[key])
      })
      return result
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

    convertUtmName (data) {
      let result = []
      data.forEach(function (item, index) {
        result.push(item['name'])
      })
      return result
    },

    createVisitSite () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'visit_site',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.visitSiteName,
        retention_days: this.visitSiteDay,

        detail: this.findSelectKey('selectUser'),
        input_percent: this.findSelectKey('selectSub')
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success;
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          alert('사이트방문 타겟 생성 실패')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    },

    createVisitSpecificPages () {
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
        var success = response.data.success;
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          alert('특정페이지 방문 타겟 생성 실패')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    },

    createNeoTarget () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'neo_target',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.neoTargetName,
        retention_days: this.neoTargetDay,
        neo_type: this.neoTargetType,

        detail: this.findSelectKey('selectUser'),
        input_percent: this.findSelectKey('selectSub')
      }

      if (this.neoTargetType === 'media') {
        params['keywords'] = this.findSelectedNeoKey('addNeoAccounts', 'accountname')
        params['neo_ids'] = this.findSelectedNeoKey('addNeoAccounts', 'param')
      } else if (this.neoTargetType === 'group') {
        params['keywords'] = this.findSelectedNeoKey('addNeoCampaigns', 'campaignname')
        params['neo_ids'] = this.findSelectedNeoKey('addNeoCampaigns', 'param')
      } else if (this.neoTargetType === 'keyword') {
        params['keywords'] = this.findSelectedNeoKey('addNeoKeywords', 'keywordname')
        params['neo_ids'] = this.findSelectedNeoKey('addNeoKeywords', 'param')
      } else {
        console.log('this.neoTargetType', this.neoTargetType)
        return
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success;
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          alert('NEO 타겟 생성 실패')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
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
        var success = response.data.success;
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
    },

    createPurchase () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'purchase',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.purchaseName,
        retention_days: this.purchaseDay,

        detail: this.findSelectKey('selectUser2'),
        purchase_count: this.purchaseCount,
        purchase_amount: this.purchaseAmount
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success;
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          alert('구매 타겟 생성 실패')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    },

    createAddToCart () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'add_to_cart',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.addToCartName,
        retention_days: this.addToCartDay,

        detail: this.findSelectKey('selectAddToCartUser')
      }

      this.$http.post('/pickdata_account_target/custom_target', params)
      .then((response) => {
        var success = response.data.success;
        if (success == "YES") {
          // success
          this.$eventBus.$emit('getAccountTarget')
        } else {
          alert('장바구니 타겟 생성 실패')
          throw('success: ' + success)
        }
        this.$emit('close')
      })
      .catch(err => {
        this.$emit('close')
        console.log('/pickdata_account_target/custom_target: ', err)
      })
    },

    createRegistration () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        target_type: 'registration',
        pixel_id: this.findSelectKey('adAccountPixels'),
        name: this.registrationName,
        retention_days: this.registrationDay,

        detail: this.findSelectKey('selectUser3'),
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
    },

    checkListNeo (elId, uniqueKey, mainListName, checkListName, addListName, selectedListName) {
      /*
      체크 된 리스트 옮기기
      (element-id, uniqueKey, 원본 리스트 저장변수, 체크된 리스트 저장변수, 옮겨진 리스트 저장변수, 선택된 리스트 저장변수)
      checkListNeo('list-neoaccount', 'centeraccountid', 'neoAccounts', 'checkDataNeoAccounts', 'addNeoAccounts', 'selectedNeoAccounts')
      */
      const me = this
      this.checkFilterNeo(elId, uniqueKey, mainListName, checkListName)

      this[addListName] = this[addListName].concat(this[checkListName])
      this[checkListName].forEach(function(value, index) {
        me[mainListName] = me[mainListName].filter(function(item) {
          return item !== value
        })
      })

      this[selectedListName] = []
      this[checkListName] = []
    },

    checkFilterNeo (elId, uniqueKey, mainListName, checkListName) {
      /*
      체크 된 리스트 저장하기
      (element-id, uniqueKey, 원본 리스트 저장변수, 체크된 리스트 저장변수)
      */
      let ul = document.getElementById(elId)
      let items = ul.getElementsByTagName("li")
      let itemsData = this[mainListName]

      for (let i = 0; i < items.length; i++) {
        let checkBox = items[i].getElementsByTagName('input')[0].checked
        if(checkBox == true) {
          let checkItemsId = items[i].getElementsByTagName('input')[0].getAttribute('data-id')
          for(let idx = 0; idx < itemsData.length ; idx++) {
            if(checkItemsId == itemsData[idx][uniqueKey]) {
              this[checkListName].push(itemsData[idx])
            }
          }
        }
      }
    },

    deleteListNeo (elId, mainListName, addListName, item) {
      /*
      선택된 리스트에서 삭제하기
      (element-id, 원본 리스트 저장변수, 옮겨진 리스트 저장변수, item Object)
      deleteListNeo('add-list-neoaccount', 'neoAccounts', 'addNeoAccounts', item)
      */
      const checkAdd = this[addListName]
      const addListEl = document.getElementById(elId)
      const addlistLi = addListEl.getElementsByTagName('li')
      if(item === 'all') {
        for(let i = 0; i < addlistLi.length; i++) {
          this[mainListName].push(checkAdd[i])
        }
        this[addListName].splice(0, addlistLi.length)
      }else{
        this[addListName].splice(this[addListName].indexOf(item), 1)
        this[mainListName].push(item)
      }
    }

  },
  computed:{
    selectAll: {
      get: function () {
        let advKeys = Object.keys(this.advs)
        if(advKeys.length != 0) {
          return this.advs ? this.selected.length == advKeys.length : false;
        }
      },
      set: function (value) {
        this.allCheck(value,'advs','selected','advs','addAdvs')
      }
    },
    selectAllNeoAccounts: {
      get () {
        let neoAccountKeys = Object.keys(this.neoAccounts)
        if (neoAccountKeys.length !== 0) {
          return this.neoAccounts ? this.selectedNeoAccounts.length === neoAccountKeys.length : false
        }
      },
      set (value) {
        let selected = []
        if (value) {
          this.checkFilterNeo('list-neoaccount', 'centeraccountid', 'neoAccounts', 'checkDataNeoAccounts')

          this.neoAccounts.forEach(function (item) {
            selected.push(item.centeraccountid)
          })
        }
        this.selectedNeoAccounts = selected
      }
    },
    selectAllNeoCampaigns: {
      get () {
        let neoCampaignKeys = Object.keys(this.neoCampaigns)
        if (neoCampaignKeys.length !== 0) {
          return this.neoCampaigns ? this.selectedNeoCampaigns.length === neoCampaignKeys.length : false
        }
      },
      set (value) {
        let selected = []
        if (value) {
          this.checkFilterNeo('list-neocampaign', 'campaignid', 'neoCampaigns', 'checkDataNeoCampaigns')

          this.neoCampaigns.forEach(function (item) {
            selected.push(item.campaignid)
          })
        }
        this.selectedNeoCampaigns = selected
      }
    },
    selectAllNeoKeywords: {
      get () {
        let neoKeywordKeys = Object.keys(this.neoKeywords)
        if (neoKeywordKeys.length !== 0) {
          return this.neoKeywords ? this.selectedNeoKeywords.length === neoKeywordKeys.length : false
        }
      },
      set (value) {
        let selected = []
        if (value) {
          this.checkFilterNeo('list-neokeyword', 'keywordid', 'neoKeywords', 'checkDataNeoKeywords')

          this.neoKeywords.forEach(function (item) {
            selected.push(item.keywordid)
          })
        }
        this.selectedNeoKeywords = selected
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
