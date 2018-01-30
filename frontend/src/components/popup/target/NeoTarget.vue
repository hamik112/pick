<template>
  <div class="target_contents_wrap clearfix" v-if="isShow">
    <transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if="dialogShow" @ok="dialogOk()" @cancel="dialogCancel()"></ui-dialog>
    </transition>
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
              <div class="result_check"><input type="radio" id="target_type04" name="neo_type" @change="wTabs(3,'wTab')" value="excel" v-model="neoTargetType"><label for="target_type04">엑셀업로드</label></div>
            </li>
          </ul>
        </div>
      </div>
      <div class="target_tbody">
        <div class="target_inner_tbody clearfix">
          <!-- 매체 -->
          <div class="cate_contents" v-if="wTab.tab1">
            <div class="account_info target_generate">
              <div class="account_title">"아래 매체로 유입된 사람" 중</div>
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
                          <ui-PartialLoading v-if="loadShow"></ui-PartialLoading>
                          <li v-for="(neoAccount, index) in neoAccounts" :key="index" v-if="!loadShow">
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
                    <li v-for="(addNeoAccount, index) in addNeoAccounts" :key="index" class="sticker_btn">
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
              <div class="account_title">"아래 그룹로 유입된 사람" 중</div>
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
                          <ui-PartialLoading v-if="loadShow"></ui-PartialLoading>
                          <li v-for="(neoCampaign, index) in neoCampaigns" :key="index" v-if="!loadShow">
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
                    <li v-for="(addNeoCampaign, index) in addNeoCampaigns" :key="index" class="sticker_btn">
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
              <div class="account_title">"아래 키워드로 유입된 사람" 중</div>
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
                          <ui-PartialLoading v-if="loadShow"></ui-PartialLoading>
                          <li v-for="(neoKeyword, index) in neoKeywords" :key="index" v-if="!loadShow">
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
                    <li v-for="(addNeoKeyword, index) in addNeoKeywords" :key="index" class="sticker_btn">
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
              <div class="account_title">"아래 등록 양식으로 유입된 사람" 중</div>
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
            <div class="account_wrap account_wrapper">
              <div class="account_inner_wrap clearfix">
                <div class="account_left">
                  <strong>양식에 맞추어 엑셀을 입력해 주세요.</strong>
                  <p>양식에 맞추어 엑셀을 업로드 해주시면,</p>
                  <p>해당 파라미터를 타겟으로 만들 수 있습니다.</p>
                  <div class="excel_wrap">
                    <div class="download_wrap clearfix">
                      <button><strong>엑셀업로드</strong></button>
                      <button @click="downloadTemplate()">양식 다운로드</button>
                    </div>
                    <div class="input_wrap clearfix">
                      <div>
                        <input type="file" @change="uploadTemplate($event)">
                      </div>
                    </div>
                    <button class="upload_btn view_alert" @click="upoloadNeoTargetFile()"><strong>업로드</strong></button>
                  </div>
                </div>
                <div class="account_right clearfix">
                  <button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../../assets/images/target/target_close_btn.png" alt=""></button>
                  <ul id="adv-list-2">
                    <li v-for="(addAdv, index) in addAdvs" :key="index" class="sticker_btn">
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
    <div v-if="makeType === 'modify'" class="modify_prologue">* 설정 수정시 기존 생성된 타겟과 병합되어 모수가 중복될 수 있습니다. 특별한 상황이 아니면 설정의 수정을 지양해주세요.</div>
    <div class="btn_wrap">
      <button class="before_btn close_pop" @click="tabMove(0)">취소</button>
      <button class="next_btn" @click="createNeoTarget()" v-if="makeType === 'add'">타겟 만들기</button>
      <button class="delete_btn" @click="deleteNeoTarget()" v-if="makeType === 'modify'">삭제</button>
      <button class="next_btn" @click="updateNeoTarget()" v-if="makeType === 'modify'">타겟 수정하기</button>
    </div>
  </div>
</template>

<script>
import { numberFormatter } from '@/components/utils/Formatter'
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'
import PartialLoading from '@/components/ui/partialLoading'

export default {
  name: 'NeoTarget',

  components: {
    'ui-select': Select,
    'ui-dialog': Dialog,
    'ui-PartialLoading': PartialLoading
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
      this.modifyNeoTargetType('media')
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
      this.modifyNeoTargetType('group')
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
        // success
      } else {
        throw('success: ' + success)
      }
      // 부분 로딩 삭제
      this.loadShow = false
      return data
    })
    .then(data => {
      data.forEach(function(item, index) {
        item['count_formatter'] = numberFormatter(item['count'])
      })
      this.neoKeywords = data
      this.modifyNeoTargetType('keyword')
    })
    .catch(err => {
      console.error('/neo_db/get_roi_report type: keyword', err)
    })
  },

  created () {
    this.$eventBus.$on('modifyNeoTarget', this.modifyNeoTarget)
  },

  beforeDestroy () {
    this.$eventBus.$off('modifyNeoTarget', this.modifyNeoTarget)
  },

  data () {
    return {
      collectionPeriod: '30',
      targetName: '',
      neoTargetType: 'media',
      audienceSize: '-',
      isNumber: false,

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

      uploadFile: '',

      subSelect: false,
      subInput: false,
      loadShow: true,

      selectCustomer: {
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

      dialogShow:false,
      dialogData:{
        emptyText:'sample',
        type:'confirm',
        mode:'sample'
      },
      nextStage:false,

      // TODO 제거 또는 변경 필요
      addAdvs:[],
      checkData:[],
      selected:[]
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

      if(mode == 'createNeoTarget') {
        // Create Target -----------------------------------------------------------------
        let params = {
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'neo_target',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,
          neo_type: this.neoTargetType,

          detail: this.findSelectKey('selectCustomer'),
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
            // 컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
            this.dialogOpen('NEO 타겟 생성 실패', 'alert')
            throw('success: ' + success)
          }
          this.$emit('close')
        })
        .catch(err => {
          this.$emit('close')
          console.log('/pickdata_account_target/custom_target: ', err)
        })

      } else if (mode === 'deleteNeoTarget') {
        // Delete Target -----------------------------------------------------------------
        this.$emit('deleteCustomTarget', this.makeItem.id)

      } else if (mode === 'updateNeoTarget') {
        // Update Target -----------------------------------------------------------------
        let params = {
          pickdata_account_target_id: this.makeItem.id,
          fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
          target_type: 'neo_target',
          pixel_id: this.findSelectKey('adAccountPixels'),
          name: this.targetName,
          retention_days: this.collectionPeriod,
          neo_type: this.neoTargetType,

          detail: this.findSelectKey('selectCustomer'),
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

        this.$http.put('/pickdata_account_target/custom_target', params)
        .then((response) => {
          var success = response.data.success
          if (success == "YES") {
            // success
            this.$eventBus.$emit('getAccountTarget')
          } else {
            this.dialogOpen('NEO  타겟 수정 실패', 'alert')
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

      // 서브 입력창 체크
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

    // Create Target Dialog
    createNeoTarget () {
      this.dialogOpen('입력한 내용으로 타겟을 생성하시겠습니까?', 'confirm', 'createNeoTarget')
    },

    // Delete Target Dialog
    deleteNeoTarget () {
      this.dialogOpen('삭제하시겠습니까?', 'confirm', 'deleteNeoTarget')
    },

    // Update Target Dialog
    updateNeoTarget () {
      this.dialogOpen('수정하시겠습니까?', 'confirm', 'updateNeoTarget')
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
    },

    modifyNeoTargetType (type) {
      const me = this
      if (this.makeType === 'modify') {
        const description = this.makeItem.description
        const params = description.params

        if (type === params.neo_type) {
          let modifyData = []
          let checkedData = []
          let neoType = params.neo_type
          let neoIds = params.neo_ids
          neoIds = Array.from(new Set(neoIds))

          this.neoTargetType = neoType
          if (neoType == 'media') {
            this.wTabs(0,'wTab')
            modifyData = this.neoAccounts
          } else if (neoType == 'group') {
            this.wTabs(1,'wTab')
            modifyData = this.neoCampaigns
          } else if (neoType == 'keyword') {
            this.wTabs(2,'wTab')
            modifyData = this.neoKeywords
          } else if (neoType == 'excel') {
            this.wTabs(3,'wTab')
          }

          neoIds.forEach(function (item, index) {
            modifyData.forEach(function (neoItem, i) {
              if (item === neoItem['param']) {
                checkedData.push(neoItem)
              }
            })
          })

          if (neoType === 'media') {
            this.checkDataNeoAccounts = checkedData
            setTimeout(function() {
              me.checkListNeo('list-neoaccount', 'centeraccountid', 'neoAccounts', 'checkDataNeoAccounts', 'addNeoAccounts', 'selectedNeoAccounts')
            }, 100)
          } else if (neoType === 'group') {
            this.checkDataNeoCampaigns = checkedData
            setTimeout(function() {
              me.checkListNeo('list-neocampaign', 'campaignid', 'neoCampaigns', 'checkDataNeoCampaigns', 'addNeoCampaigns', 'selectedNeoCampaigns')
            }, 100)
          } else if (neoType === 'keyword') {
            this.checkDataNeoKeywords = checkedData
            // this.checkFilterNeo('list-neokeyword', 'keywordid', 'neoKeywords', 'checkDataNeoKeywords')
            setTimeout(function() {
              me.checkListNeo('list-neokeyword', 'keywordid', 'neoKeywords', 'checkDataNeoKeywords', 'addNeoKeywords', 'selectedNeoKeywords')
            }, 100)

          } else if (neoType === 'excel') {
            // Nothing
          }
        }
      }
    },

    modifyNeoTarget () {
      const description = this.makeItem.description
      const params = description.params
      const detail = params.detail

      // 사용 픽셀
      this.adAccountPixels.emptyText = this.findSelectText('adAccountPixels', this.makeItem.description.params.pixel_id)

      // 수집 기간
      this.collectionPeriod = numberFormatter(this.makeItem.description.retention_days)

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
        this.selectCustomer.emptyText = '구매 고객'
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
    },

    downloadTemplate () {
      window.open('/pickdata_account_target/neo_custom_target', '_blank')
    },

    uploadTemplate (event) {
      console.log(event.target)
      console.log(event.target.files[0])
      this.uploadFile = event.target.files[0]
    },

    upoloadNeoTargetFile () {
      let params = {
        fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
        upload_file: this.uploadFile
      }

      if (this.uploadFile == '') {
        this.dialogOpen('업로드 파일이 없습니다.', 'alert')
        return
      }

      this.$http.post('/pickdata_account_target/neo_custom_target', params)
      .then((response) => {
        var success = response.data.success
        if (success == "YES") {
          // success
          console.log('success')
        } else {
          throw('success: ' + success)
        }
      })
      .catch(err => {
        // this.$emit('close')
        console.log('/pickdata_account_target/neo_custom_target: ', err)
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
