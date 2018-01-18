<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="ad_set_pop_1">
						<div class="popup-contents">
							<div class="pop_title_wrap">
								<div class="pop_title">광고계정 설정하기</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="ad_info_wrap">
								<div class="ad_mask"></div>
								<div class="ad_image"><img src="../../assets/images/common/test_img.jpg" alt=""></div>
								<div class="ad_info">
									<strong>프리메라 NEW</strong>
									<div>계정번호:1059484622123515</div>
								</div>
							</div>
							<div class="list-tab-widget">
								<div class="tab-nav-widget">
									<ul>
										<li rel="tab-list-1" v-bind:class="[(this.tabListStep === 0) ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>1</span>카테고리 설정</a>
										</li>
										<li rel="tab-list-2" v-bind:class="[(this.tabListStep === 1) ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>2</span>네오 계정 연동</a>
										</li>
										<li rel="tab-list-3" v-bind:class="[(this.tabListStep === 2) ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>3</span>픽셀 이벤트 매핑</a>
										</li>
									</ul>
								</div>
								<div class="pop_tab_wrap">
									<div class="tab-contents-widget">

										<!-- 카테고리 설정 -->
										<div id="tab-list-1" class="basic-tab-contents category_setup clearfix" v-if='tabActive1'>
											<div class="cate_prologue">
												<strong>현재 선택된 광고 계정의 카테고리를 지정해주세요</strong>
												<p>통계 및 계정 유형 분석을 위해 반드시 선택하셔야 합니다.</p>
											</div>
											<div class="cate_contents_widget">
												<ul class="target_pick_01">
													<li @click="clickSteop1Category('보험')" v-bind:class="[(this.categoryName === '보험') ? 'Click_on' : '']">
														<span>보험</span>
													</li>
													<li @click="clickSteop1Category('대출')" v-bind:class="[(this.categoryName === '대출') ? 'Click_on' : '']">
														<span>대출</span>
													</li>
													<li @click="clickSteop1Category('카드')" v-bind:class="[(this.categoryName === '카드') ? 'Click_on' : '']">
														<span>카드</span>
													</li>
													<li @click="clickSteop1Category('NGO')" v-bind:class="[(this.categoryName === 'NGO') ? 'Click_on' : '']">
														<span>NGO</span>
													</li>
												</ul>
												<ul class="target_pick_02">
													<li @click="clickSteop1Category('쇼핑몰')" v-bind:class="[(this.categoryName === '쇼핑몰') ? 'Click_on' : '']">
														<span>쇼핑몰</span>
													</li>
													<li @click="clickSteop1Category('여행')" v-bind:class="[(this.categoryName === '여행') ? 'Click_on' : '']">
														<span>여행</span>
													</li>
													<li @click="clickSteop1Category('뷰티')" v-bind:class="[(this.categoryName === '뷰티') ? 'Click_on' : '']">
														<span>뷰티</span>
													</li>
													<li @click="clickSteop1Category('기타')" v-bind:class="[(this.categoryName === '기타') ? 'Click_on' : '']">
														<span>기타</span>
													</li>
												</ul>
											</div>
											<div class="btn_wrap">
												<button type="button" class="next_btn" @click="tabMove('1', '0')">다음</button>
											</div>
										</div>
										<!-- /.카테고리 설정 -->


										<!-- 네오 계정 연동 -->
										<div id="tab-list-2" class="basic-tab-contents clearfix" v-if='tabActive2'>
											<div class="cate_prologue">
												<strong>연결될 네오 계정을 선택해 주세요.</strong>
												<p>연결 가능한 네오 계정이 없다면 다음을 클릭해 주세요.</p>
											</div>

											<div class="cate_contents">
												<div class="account_wrap">
													<div class="advertiser_search">
														<div class="search_title">광고주검색</div>
														<div><input type="text" v-model="searchKeyword" placeholder="광고주를 검색하세요."></div>
														<div><button type="button" @click="listSearch()">조회</button></div>
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
												<div class="interlock_btn">
													<button type="button" title="삭제" @click="checkList('addedAdvs', 'advs')"><img src="../../assets/images/icon/account_left.jpg" alt=""></button>
													<button type="button" title="추가" @click="checkList('advs', 'addedAdvs')"><img src="../../assets/images/icon/account_right.jpg" alt=""></button>
												</div>
												<div class="account_wrap">
													<div class="advertiser_search">
														<div class="search_title">연결계정 <span id="ct-count">{{ this.ctCount }}</span></div>
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
																	<li v-for="addedAdv in addedAdvs" :key="addedAdv.id">
																		<div class="result_check"><input type="checkbox" v-model="addSelected" :value="addedAdv.id" class="result-checkbox" :data-type="'addedAdvs'" :data-id="addedAdv.type_id" :id="'addedAdv-check-' + addedAdv.id"><label :for="'addedAdv-check-' + addedAdv.id"></label></div>
																		<div class="result_advertiser">{{ addedAdv.name }}</div>
																		<div class="result_account">{{ addedAdv.advid }}</div>
																	</li>
																</ul>
															</div>
														</div>
													</div>
												</div>
											</div>


											<div class="btn_wrap">
												<button class="before_btn" @click="tabMove('0', '1')">이전</button>
												<button type="button" class="next_btn" @click="tabMove('2', '1')">다음</button>
											</div>
										</div>
										<!-- /.네오 계정 연동 -->



										<!-- 픽셀 이벤트 매핑 -->
										<div id="tab-list-3" class="basic-tab-contents clearfix" v-if='tabActive3'>
											<div class="cate_prologue">
												<strong>광고 계정에 사용된 픽셀 이벤트를 매핑해 주세요.</strong>
												<p>픽셀 이벤트를 매핑해 주시면, 좀 더 편리한 맞춤 타겟팅을 사용할 수 있습니다.</p>
											</div>
											<div class="event_mapping_wrap">
												<ul>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
													<li class="select_btn">
														<div class="select_title">구매</div>
														<div class="select_contents">
															<div><ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select></div>
														</div>
													</li>
												</ul>
												<div class="btn_wrap">
													<button type="button" class="before_btn" @click="tabMove('1', '2')">이전</button>
													<button class="next_btn" @click="success">완료</button>
												</div>
											</div>
										</div>
										<!-- /.픽셀 이벤트 매핑 -->


									</div>
								</div>
							</div>
							<p class="popup-btn"><button type="button" id="close-btn" class="close-btn close_pop"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
//UI
import Select from '@/components/ui/Select'

export default {
	name:'SetupPop',

	components:{
		'ui-select':Select
	},

	created() {
		this.$http.get('/api/neo_db/search_neo_accounts?adv_name')
			.then(res => {
				const total_count = res.data.total_count
				const data = res.data

				for(let i = 0; i < total_count; i++) {
					this.advs.push({
						// 데이터
						id: data.data[i].centeraccountid,
						advertiserid: data.data[i].advertiserid,
						type_id: data.data[i].centeraccountid,
						// 화면
						name: data.data[i].advertisername,
						advid: data.data[i].accountnickname,
					})
				}
			})
			.catch(err => {
				console.log(err)
			})
	},

	data () {
		return {
			tabActive1: true,
			tabActive2: false,
			tabActive3: false,

			categorySelectData: {
				emptyText: '픽셀 이벤트를 선택해주세요',
				textList: [
					'픽셀1',
					'픽셀2',
					'픽셀3'
				]
			},
			advs: [],
			addedAdvs:[],
			checkData:[],
			addKey:[],
			selected: [],
			addSelected:[],

			tabListStep: 0,
			ctCount:0,
			categoryName: '',

			searchKeyword: '',
		}
	},

	methods:{
		clickSteop1Category (name) {
			this.categoryName = name
		},
		selectCategory (item) {
			this.categorySelectData.emptyText = item
		},
		listSearch() {
			//리스트 검색시 노출
			this.advs = [
				{ "id": "1", "name": "LF몰", "advid": "LF_M_구글1", "type_id":"13" },
			    { "id": "2", "name": "LF몰2", "advid": "LF_M_구글2", "type_id":"11" },
			    { "id": "3", "name": "LF몰3", "advid": "LF_M_구글3", "type_id":"15" },
			    { "id": "4", "name": "LF몰4", "advid": "LF_M_구글4", "type_id":"17" }
			]

		},
		listSort(item) {
			const me = this
			let checkData = me.checkData

		},
		checkFilter (currentList) {
			// this[currentList] === this['advs' || 'addedAdvs']
			let items = this[currentList]

			let neoAccountList    = (currentList == 'advs') ? "adv-list-1" : "adv-list-2"
			let linkedAccountList = (currentList != 'advs') ? "adv-list-1" : "adv-list-2"

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
							this.checkData.push(items[i])
						}
					}
				}
			}
		},
		checkList (before, after) {
			const me = this

			this.checkFilter(before)

			this[after] = this[after].concat(this.checkData)
			this.checkData.forEach(value => {
				me[before] = me[before].filter(item => {
					return item !== value
				})
			})

			// 연결 계정 리스트 개수
			this.ctCount = this.addedAdvs.length
			document.getElementById('ct-count').innerText = this.ctCount

			this.addSelected = []
			this.selected = []
			this.checkData = []
		},
		allCheck(value,key1,key2,before,after) {
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
		tabMove (activeNumber, beforeNumber) {
			if (beforeNumber === '0') {
				if (this.categoryName === '') {
					alert('통계 및 계정 유형 분석을 선택해주세요.')
					return false
				} else {
					console.log("선택된 페이스북 광고 계정: ", this.currentFbAdAccount.id)

					let actAccountId = this.currentFbAdAccount.id;
					let accountCategoryId = 0

					if(this.categoryName === '대출') {
						accountCategoryId = 1
					} else if(this.categoryName === 'NGO') {
						accountCategoryId = 2
					} else if(this.categoryName === '카드') {
						accountCategoryId = 3
					} else if(this.categoryName === '여행') {
						accountCategoryId = 4
					} else if(this.categoryName === '쇼핑몰') {
						accountCategoryId = 5
					} else if(this.categoryName === '기타') {
						accountCategoryId = 6
					} else if(this.categoryName === '보험') {
						accountCategoryId = 7
					} else if(this.categoryName === '뷰티') {
						accountCategoryId = 8
					}
					this.$http.post('/api/fb_ad_accounts/', {
							act_account_id: actAccountId,
							account_category_id: accountCategoryId,
					})
					.then(res => {
							localStorage.setItem('fb_ad_account_id', res.data.data.id)
					})
				}
			}else if(activeNumber == '2' && beforeNumber === '1') {
				if(this.addedAdvs.length == 0) {
					if(confirm('선택된 네오 계정이 없습니다. 계속 진행하시겠습니까?') === false) {
						return false
					}
				} else {
					console.log(this.currentFbAdAccount.id)
					console.log(this.addedAdvs)

					let neoAdvIds = []
					let neoAccountIds = []

					// 추가된 네오 계정 리스트
					for(let i = 0; i < this.addedAdvs.length; i++) {
						neoAdvIds.push(this.addedAdvs[i].advertiserid)
						neoAccountIds.push(this.addedAdvs[i].id)
					}

					console.log(this.$store.state.currentFbAdAccount.account_id)
					console.log('fb_ad_account_id: ' + localStorage.getItem('fb_ad_account_id'))
					console.log(neoAdvIds)
					console.log(neoAccountIds)

					this.$http.post('/api/neo_account/', {
						fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
						neo_adv_ids: neoAdvIds,
						neo_account_ids: neoAccountIds 
					})
				}
			}
			this.tabListStep = parseInt(activeNumber)
			let tabArray = ['tabActive1','tabActive2','tabActive3']
			for(let i = 0; i < tabArray.length; i++) {
				if(i == activeNumber) {
					this[tabArray[i]] = true
				}else{
					this[tabArray[i]] = false
				}
			}
		},
		success () {
			if(confirm('현재 매칭된 상태로 Target Pick 설정을 진행할까요?') === true) {
				this.$emit('close')
			}else{
				return false
			}
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
                this.allCheck(value,'advs','selected','advs','addedAdvs')
            }
		},
		addSelectAll:{
				get: function () {
					let advKeys = Object.keys(this.addedAdvs)
					if(advKeys.length != 0) {
							return this.addedAdvs ? this.addSelected.length == advKeys.length : false;
						}
				},
				set: function (value) {
						this.allCheck(value,'addedAdvs','addSelected','addedAdvs','advs')
				}
		},
		currentFbAdAccount() {
			return this.$store.state.currentFbAdAccount
		},
		searchedAdvs() {
			if(this.searchKeyword === '') {
				// 키워드가 없을때, 전체 리스트 반환
				return this.advs
			} else {
				// 키워드를 포함한, 리스트 반환
				return this.advs.filter(adv => {
					return adv.name.match(this.searchKeyword)
				})
			}
		}
	}
}
</script>

<style lang="css" scoped>
</style>
