<template>
  <div class="target_contents_wrap pop-scroll clearfix" v-if="isShow">
    <div class="target_contents_inner">
      <div class="target_thead">
        <div class="main_title">
          <div><img src="../../../assets/images/target/target_logo_03.png" alt="neo"></div>
          <div class="title_info">
            <p>NEO타겟</p>
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
            <div><input type="text" v-model="neoTargetDay"><span>일</span></div>
          </div>
        </div>
        <div class="target_name">
          <div class="contents_title">타겟이름</div>
          <div><input type="text" v-model="neoTargetName"></div>
        </div>
        <div class="target_type">
          <div class="contents_title">Neo 유형</div>
          <ul>
            <li>
              <div class="result_check"><input type="radio" id="target_type01" @change="wTabs(0,'wTab')" name="neo_type" value="media" v-model="neoTargetType" checked><label for="target_type01">매체</label></div>
            </li>
            <li>
              <div class="result_check"><input type="radio" id="target_type02" name="neo_type" @change="wTabs(1,'wTab')" value="group" v-model="neoTargetType"><label for="target_type02">그룹</label></div>
            </li>
            <li>
              <div class="result_check"><input type="radio" id="target_type03" name="neo_type"  @change="wTabs(2,'wTab')" value="keyword" v-model="neoTargetType"><label for="target_type03">키워드</label></div>
            </li>
            <li>
              <div class="result_check" v-show="false"><input type="radio" id="target_type04" name="neo_type" @change="wTabs(3,'wTab')" value="excel" v-model="neoTargetType"><label for="target_type04">엑셀업로드</label></div>
            </li>
          </ul>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <!-- 매체 -->
          <div class="cate_contents" v-if="wTab.tab1">
            <div class="account_info target_generate">
              <div class="account_title">"아래 매체로 유입된 사람"중</div>
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
            <div class="account_wrap account_wrapper">
              <div class="account_inner_wrap clearfix">
                <div class="account_left">
                  <div class="advertiser_search_result pop-scroll">
                    <div class="result_list_inner">
                      <div class="result_thead">
                        <ul>
                          <li>
                            <div class="result_check"><input type="checkbox" id="all_check" v-model="selectAllNeoAccounts"><label for="all_check"></label></div>
                            <div class="result_account">광고주명</div>
                            <div class="result_group">매체명</div>
                            <div class="result_switch">전환 수</div>
                          </li>
                        </ul>
                      </div>
                      <div class="result_tbody">
                        <ul id="list-neoaccount">
                          <li v-for="neoAccount in neoAccounts">
                            <div class="result_check"><input type="checkbox" v-model="selectedNeoAccounts" :value="neoAccount.centeraccountid" class="result-checkbox" :data-type="'neoAccounts'" :data-id="neoAccount.centeraccountid" :id="'neoAccount-check-' + neoAccount.centeraccountid"><label :for="'neoAccount-check-' + neoAccount.centeraccountid"></label></div>
                            <div class="result_account">{{ neoAccount.advname }}</div>
                            <div class="result_group">{{ neoAccount.accountname }}</div>
                            <div class="result_switch">{{ neoAccount.count_formatter }}</div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <div class="account_add_wrap">
                    <div>*최근 한달 기준</div>
                    <button type="button" v-on:click="checkListNeo('list-neoaccount', 'centeraccountid', 'neoAccounts', 'checkDataNeoAccounts', 'addNeoAccounts', 'selectedNeoAccounts')">선택한 매체 추가</button>
                  </div>
                </div>
                <div class="account_right clearfix">
                  <button type="button" v-on:click="deleteListNeo('add-list-neoaccount', 'neoAccounts', 'addNeoAccounts', 'all')" title="전체삭제"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button>
                  <ul id="add-list-neoaccount">
                    <li v-for="addNeoAccount in addNeoAccounts" class="sticker_btn">
                      <span>{{ addNeoAccount.accountname }}</span> <span @click="deleteListNeo('add-list-neoaccount', 'neoAccounts', 'addNeoAccounts', addNeoAccount)" :data-number="addNeoAccount.centeraccountid" title="삭제하기"><img src="../../../assets/images/target/target_list_close.png" alt=""></span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <!-- 그룹 -->
          <div class="cate_contents" v-if="wTab.tab2">
            <div class="account_info target_generate">
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
            <div class="account_wrap account_wrapper">
              <div class="account_inner_wrap clearfix">
                <div class="account_left">
                  <div class="advertiser_search_result pop-scroll">
                    <div class="result_list_inner">
                      <div class="result_thead">
                        <ul>
                          <li>
                            <div class="result_check"><input type="checkbox" id="all_check" v-model="selectAllNeoCampaigns"><label for="all_check"></label></div>
                            <div class="result_account">광고주명</div>
                            <div class="result_group">그룹명</div>
                            <div class="result_switch">전환 수</div>
                          </li>
                        </ul>
                      </div>
                      <div class="result_tbody">
                        <ul id="list-neocampaign">
                          <li v-for="neoCampaign in neoCampaigns">
                            <div class="result_check"><input type="checkbox" v-model="selectedNeoCampaigns" :value="neoCampaign.campaignid" class="result-checkbox" :data-type="'neoCampaigns'" :data-id="neoCampaign.campaignid" :id="'neoCampaign-check-' + neoCampaign.campaignid"><label :for="'neoCampaign-check-' + neoCampaign.campaignid"></label></div>
                            <div class="result_account">{{ neoCampaign.advname }}</div>
                            <div class="result_group">{{ neoCampaign.campaignname }}</div>
                            <div class="result_switch">{{ neoCampaign.count_formatter }}</div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <div class="account_add_wrap">
                    <div>*최근 한달 기준</div>
                    <button type="button" v-on:click="checkListNeo('list-neocampaign', 'campaignid', 'neoCampaigns', 'checkDataNeoCampaigns', 'addNeoCampaigns', 'selectedNeoCampaigns')">선택한 매체 추가</button>
                  </div>
                </div>
                <div class="account_right clearfix">
                  <button type="button" v-on:click="deleteListNeo('add-list-neocampaign', 'neoCampaigns', 'addNeoCampaigns', 'all')" title="전체삭제"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button>
                  <ul id="add-list-neocampaign">
                    <li v-for="addNeoCampaign in addNeoCampaigns" class="sticker_btn">
                      <span>{{ addNeoCampaign.campaignname }}</span> <span @click="deleteListNeo('add-list-neocampaign', 'neoCampaigns', 'addNeoCampaigns', addNeoCampaign)" :data-number="addNeoCampaign.campaignid" title="삭제하기"><img src="../../../assets/images/target/target_list_close.png" alt=""></span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <!-- 키워드 -->
          <div class="cate_contents" v-if="wTab.tab3">
            <div class="account_info target_generate">
              <div class="account_title">"아래 키워드로 유입된 사람"중</div>
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
            <div class="account_wrap account_wrapper">
              <div class="account_inner_wrap clearfix">
                <div class="account_left">
                  <div class="advertiser_search_result pop-scroll">
                    <div class="result_list_inner">
                      <div class="result_thead">
                        <ul>
                          <li>
                            <div class="result_check"><input type="checkbox" id="all_check" v-model="selectAllNeoKeywords"><label for="all_check"></label></div>
                            <div class="result_account">광고주명</div>
                            <div class="result_group">키워드</div>
                            <div class="result_switch">전환 수</div>
                          </li>
                        </ul>
                      </div>
                      <div class="result_tbody">
                        <ul id="list-neokeyword">
                          <li v-for="neoKeyword in neoKeywords">
                            <div class="result_check"><input type="checkbox" v-model="selectedNeoKeywords" :value="neoKeyword.keywordid" class="result-checkbox" :data-type="'neoKeywords'" :data-id="neoKeyword.keywordid" :id="'neoKeyword-check-' + neoKeyword.keywordid"><label :for="'neoKeyword-check-' + neoKeyword.keywordid"></label></div>
                            <div class="result_account">{{ neoKeyword.advname }}</div>
                            <div class="result_group">{{ neoKeyword.keywordname }}</div>
                            <div class="result_switch">{{ neoKeyword.count_formatter }}</div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <div class="account_add_wrap">
                    <div>*최근 한달 기준</div>
                    <button type="button" v-on:click="checkListNeo('list-neokeyword', 'keywordid', 'neoKeywords', 'checkDataNeoKeywords', 'addNeoKeywords', 'selectedNeoKeywords')">선택한 매체 추가</button>
                  </div>
                </div>
                <div class="account_right clearfix">
                  <button type="button" v-on:click="deleteListNeo('add-list-neokeyword', 'neoKeywords', 'addNeoKeywords', 'all')" title="전체삭제"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button>
                  <ul id="add-list-neokeyword">
                    <li v-for="addNeoKeyword in addNeoKeywords" class="sticker_btn">
                      <span>{{ addNeoKeyword.keywordname }}</span> <span @click="deleteListNeo('add-list-neokeyword', 'neoKeywords', 'addNeoKeywords', addNeoKeyword)" :data-number="addNeoKeyword.keywordid" title="삭제하기"><img src="../../../assets/images/target/target_list_close.png" alt=""></span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <!-- 엑셀 -->
          <div class="cate_contents target_excel" v-if="wTab.tab4">
            <div class="account_info target_generate">
              <div class="account_title">"아래 등록 양식으로 유입된 사람"중</div>
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
            <div class="account_wrap account_wrapper">
              <div class="account_inner_wrap clearfix">
                <div class="account_left">
                  <strong>양식에 맞추어 엑셀을 입력해 주세요.</strong>
                  <p>양식에 맞추어 엑셀을 업로드 해주시면,</p>
                  <p>해당 파라미터를 타겟으로 만들 수 있습니다.</p>
                  <div class="excel_wrap">
                    <div class="download_wrap clearfix">
                      <button><strong>엑셀업로드</strong></button>
                      <button>양식 다운로드</button>
                    </div>
                    <div class="input_wrap clearfix">
                      <div>
                        <input type="text">
                      </div>
                      <button></button>
                    </div>
                    <button class="upload_btn view_alert"><strong>업로드</strong></button>
                  </div>
                </div>
                <div class="account_right clearfix">
                  <button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button>
                  <ul id="adv-list-2">
                    <li v-for="addAdv in addAdvs" class="sticker_btn">
                      <span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../../assets/images/target/target_list_close.png" alt=""></span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createNeoTarget()">타겟 만들기</button>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
import Select from '@/components/ui/Select'

export default {
  name: 'NeoTarget',

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

  computed:{
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
  },

  mounted () {
    this.$http.get('/neo_db/get_roi_report', {
      params: {
        'fb_ad_account_id': localStorage.getItem('fb_ad_account_id'),
        'type': 'account'
      }
    })
    .then(res => {
      const response = res.data
      const data = response.data
      const success = response.success
      if (success === 'YES') {
        // success
      } else {
        throw('success: ' + success)
      }
      return data
    })
    .then(data => {
      data.forEach(function(item, index) {
        item['count_formatter'] = numberFormatter(item['count'])
      })
      this.neoAccounts = data
    })
    .catch(err => {
      console.error('/neo_db/get_roi_report type: account ', err)
    })

    this.$http.get('/neo_db/get_roi_report', {
      params: {
        'fb_ad_account_id': localStorage.getItem('fb_ad_account_id'),
        'type': 'campaign'
      }
    })
    .then(res => {
      const response = res.data
      const data = response.data
      const success = response.success
      if (success === 'YES') {
        // success
      } else {
        throw('success: ' + success)
      }
      return data
    })
    .then(data => {
      data.forEach(function(item, index) {
        item['count_formatter'] = numberFormatter(item['count'])
      })
      this.neoCampaigns = data
    })
    .catch(err => {
      console.error('/neo_db/get_roi_report type: campaign ', err)
    })

    this.$http.get('/neo_db/get_roi_report', {
      params: {
        'fb_ad_account_id': localStorage.getItem('fb_ad_account_id'),
        'type': 'keyword'
      }
    })
    .then(res => {
      const response = res.data
      const data = response.data
      const success = response.success
      if (success === 'YES') {
        // success~
      } else {
        throw('success: ' + success)
      }
      return data
    })
    .then(data => {
      data.forEach(function(item, index) {
        item['count_formatter'] = numberFormatter(item['count'])
      })
      this.neoKeywords = data
    })
    .catch(err => {
      console.error('/neo_db/get_roi_report type: keyword', err)
    })
  },

  data () {
    return {
      neoTargetDay: '30',
      neoTargetName: '',
      neoTargetType: 'media',

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

      subSelect:false,
      subInput:false,

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

      wTab: {
        tab1: true,
        tab2: false,
        tab3: false,
        tab4: false,
        tab5: false,
        tab6: false
      },

      // TODO 제거 또는 변경 필요
      addAdvs:[],
      checkData:[],
      selected:[]
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

    findSelectedNeoKey (listName, key) {
      let result = []
      const data = this[listName]
      data.forEach(function (item, index) {
        result.push(item[key])
      })
      return result
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
        var success = response.data.success
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

    // TODO 제거 또는 변경 필요
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
