<template>
  <div id="tab-list-2" class="basic-tab-contents clearfix">
  	<transition name="modal">
	  <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
	</transition>
    <div class="cate_prologue">
      <strong>연결될 네오 계정을 선택해 주세요.</strong>
      <p>연결 가능한 네오 계정이 없다면 다음을 클릭해 주세요.</p>
    </div>
    <!-- 전체 네오 계정 리스트 -->
    <div class="cate_contents">
      <div class="account_wrap">
        <div class="advertiser_search">
          <div class="search_title">광고주검색</div>
          <div><input type="text" v-model="searchKeyword" placeholder="광고주를 검색하세요."></div>
          <div><button type="button">조회</button></div>
        </div>
        <div class="advertiser_search_result pop-scroll">
          <div>
            <div class="result_thead">
              <ul>
                <li>
                  <div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
                  <div class="result_advertiser">광고주</div>
                  <div class="result_account">계정명</div>
                </li>
              </ul>
            </div>
            <div class="result_tbody">
              <ul id="adv-list-1">
                <li v-for="adv in searchedAdvs" :key="adv.id">
                  <div class="result_check"><input type="checkbox" v-model="selected" :value="adv.id" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.id"><label :for="'adv-check-' + adv.id"></label></div>
                  <div class="result_advertiser">{{ adv.name }}</div>
                  <div class="result_account">{{ adv.advid }}</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- 추가 / 삭제 -->
      <div class="interlock_btn">
        <button type="button" title="삭제" @click="checkList('linkedAdvs', 'advs')"><img src="../../../assets/images/icon/account_left.jpg" alt=""></button>
        <button type="button" title="추가" @click="checkList('advs', 'linkedAdvs')"><img src="../../../assets/images/icon/account_right.jpg" alt=""></button>
      </div>
      <!-- 연결된 네오 계정 리스트 -->
      <div class="account_wrap">
        <div class="advertiser_search">
          <div class="search_title">연결계정<span id="ct-count">{{ linkedAdvs.length }}</span></div>
        </div>
        <div class="advertiser_search_result pop-scroll">
          <div>
            <div class="result_thead">
              <ul>
                <li>
                  <div class="result_check"><input type="checkbox" id="right_all_check" v-model="addSelectAll"><label for="right_all_check"></label></div>
                  <div class="result_advertiser">광고주</div>
                  <div class="result_account">계정명</div>
                </li>
              </ul>
            </div>
            <div class="result_tbody">
              <ul id="adv-list-2">
                <li v-for="linkedAdv in linkedAdvs" :key="linkedAdv.id">
                  <div class="result_check"><input type="checkbox" v-model="addSelected" :value="linkedAdv.id" class="result-checkbox" :data-type="'linkedAdvs'" :data-id="linkedAdv.type_id" :id="'linkedAdv-check-' + linkedAdv.id"><label :for="'linkedAdv-check-' + linkedAdv.id"></label></div>
                  <div class="result_advertiser">{{ linkedAdv.name }}</div>
                  <div class="result_account">{{ linkedAdv.advid }}</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- 이전 / 다음 -->
      <div class="btn_wrap">
        <button class="before_btn" @click="backToSetCategory()">이전</button>
        <button type="button" class="next_btn" @click="setNeoAccountLinkage('step2')">다음</button>
      </div>
    </div>
  </div>
</template>

<script>

import Dialog from '@/components/ui/Dialog'

export default {
  components:{
  	'ui-dialog':Dialog
  },
  created () {
		// 네오 계정 리스트
		this.$http.get('/neo_db/search_neo_accounts?adv_name')
			.then(res => {
				const totalCount = res.data.total_count
				const data = res.data.data

				for(let i = 0; i < totalCount; i++) {
					this.advs.push({
						// 데이터
						id: data[i].centeraccountid,
						advertiserid: data[i].advertiserid,
						type_id: data[i].centeraccountid,
						// 화면
						name: data[i].advertisername,
						advid: data[i].accountnickname,
					})
				}
			})
			.catch(err => {
				console.log(err)
			})

		// 연결된 네오 계정 리스트
		this.$http.get('/neo_account/', {
			params: {fb_ad_account_id: localStorage.getItem('fb_ad_account_id')}
		})
		.then(res => {
			const totalCount = res.data.count
			const data = res.data.data

			for(let i = 0; i < totalCount; i++) {
				this.linkedAdvs.push({
					// 데이터
					id: data[i].neo_account_id,
					advertiserid: data[i].neo_adv_id,
					type_id: data[i].neo_account_id,
					// 화면
					name: data[i].neo_adv_name,
					advid: data[i].neo_account_name,
				})
			}
		})
  },

  data () {
    return {
			dialogShow:false,
			dialogData:{
				emptyText:'sample',
				type:'confirm',
				mode:'sample'
			},
			nextStage:false,
			neoAdvIds: [],
			neoAccountIds: [],
			advs: [],
			linkedAdvs:[],
			checkedAdvs:[],
			searchKeyword: '',
			selected: [],
			addSelected:[],
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

			//모드별 동작
			if(mode == 'step2') {
				//다음스텝
				this.setNeoAccountLinkageNextStep()
			}

			this.nextStage = true
			this.dialogShow = false;
		},
		dialogCancel() {
			this.nextStage = false;
			this.dialogShow = false;
		},


		checkFilter (beforeAdvs) {
			// this[beforeAdvs] === this['advs' || 'linkedAdvs']
			let items = this[beforeAdvs]

			let neoAccountList    = (beforeAdvs == 'advs') ? "adv-list-1" : "adv-list-2"
			let linkedAccountList = (beforeAdvs != 'advs') ? "adv-list-1" : "adv-list-2"

			let neoAccountListItems    = document.getElementById(neoAccountList).getElementsByTagName('li')
			let linkedAccountListItems = document.getElementById(linkedAccountList).getElementsByTagName('li')

			for(let i = 0; i < linkedAccountListItems.length; i++) {
				// 연결된 네오 계정 리스트 체크 전체 해제
				linkedAccountListItems[i].getElementsByTagName('input')[0].checked = false
			}

			for (let i = 0; i < neoAccountListItems.length; i++) {
				// 네오 계정 리스트 체크 유/무
				let isChecked = neoAccountListItems[i].getElementsByTagName('input')[0].checked

				if(isChecked === true) {
					// 네오 계정 리스트가 체크 되어있을 경우
					let checkedItemId = neoAccountListItems[i].getElementsByTagName('input')[0].getAttribute('data-id')

					for(let i = 0; i < items.length; i++) {
						if(checkedItemId == items[i]['type_id']) {
							this.checkedAdvs.push(items[i])
						}
					}
				}
			}
		},

		checkList (beforeAdvs, afterAdvs) {
			const me = this
			this.checkFilter(beforeAdvs)

			if(afterAdvs === 'advs') {
				// 연결된 계정을 제외한 네오 계정 리스트에 연결 해제된 advs(=checkedAdvs)를 맨 뒤에 추가
				this[afterAdvs] = this.searchedAdvs.concat(this.checkedAdvs)
			} else {
				// 연결할 네오 계정 리스트 맨 뒤에 추가
				this[afterAdvs] = this[afterAdvs].concat(this.checkedAdvs)
			}

			this.checkedAdvs.forEach(checkedAdv => {
				me[beforeAdvs] = me[beforeAdvs].filter(beforeAdv => {
					return beforeAdv !== checkedAdv
				})
			})

			// 연결 계정 리스트 개수
			document.getElementById('ct-count').innerText = this.linkedAdvs.length

			this.addSelected = []
			this.selected = []
			this.checkedAdvs = []
		},

		allCheck (value, key1, key2, before, after) {
			const me = this
			var selected = []
			if (value) {
				this.checkFilter(key1)
				me[key1].forEach(function (item) {
					selected.push(item.id)
				});
			}
			me[key2] = selected;
		},

    backToSetCategory () {
      let currentStep = [true, false, false]
      this.$emit('backToSetCategory', currentStep)
    },

    setNeoAccountLinkage (mode) {
      if(this.linkedAdvs.length == 0) {
      	//컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
      	this.dialogOpen('선택된 네오 계정이 없습니다. 계속 진행하시겠습니까?', 'confirm', mode)
      } else {
        // 추가된 네오 계정 리스트
        for(let i = 0; i < this.linkedAdvs.length; i++) {
          this.neoAdvIds.push(this.linkedAdvs[i].advertiserid)
          this.neoAccountIds.push(this.linkedAdvs[i].id)
        }
        this.setNeoAccountLinkageNextStep()
      }
    },
	setNeoAccountLinkageNextStep() {
		let currentStep = [false, false, true]
      	this.$emit('setNeoAccountLinkage', currentStep, this.neoAdvIds, this.neoAccountIds)
	}
  },

  computed: {
		selectAll: {
			get: function () {
				let advKeys = Object.keys(this.advs)
				if(advKeys.length != 0) {
					return this.advs ? this.selected.length == advKeys.length : false;
				}
			},
			set: function (value) {
				this.allCheck(value, 'advs', 'selected', 'advs', 'linkedAdvs')
			}
		},

    addSelectAll:{
			get: function () {
				let advKeys = Object.keys(this.linkedAdvs)
				if(advKeys.length != 0) {
					return this.linkedAdvs ? this.addSelected.length == advKeys.length : false;
				}
			},
			set: function (value) {
				this.allCheck(value, 'linkedAdvs', 'addSelected', 'linkedAdvs', 'advs')
			}
		},

    searchedAdvs() {
			// 연결된 계정 아이디
			let linkedAdvIds = []
			for(let i = 0; i < this.linkedAdvs.length; i++) {
				linkedAdvIds.push(this.linkedAdvs[i].id)
			}

			if(this.searchKeyword === '') {
				// 키워드가 없을때, 전체 리스트 반환(연결된 계정 제외)
				return this.advs.filter(adv => {
					return !linkedAdvIds.includes(adv.id)
				})
			} else {
				// 키워드를 포함한, 리스트 반환(연결된 계정 제외)
				let searchResultAdvs = this.advs.filter(adv => {
					return adv.name.match(this.searchKeyword)
				})

				return searchResultAdvs.filter(searchResultAdv => {
					return !linkedAdvIds.includes(searchResultAdv.id)
				})
			}
		}
  }
}
</script>

<style>

</style>
