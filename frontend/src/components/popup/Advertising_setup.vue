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
									<strong>{{ this.currentFbAdAccount.name }}</strong>
									<div>계정번호:{{ this.currentFbAdAccount.account_id }}</div>
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
													<button type="button" title="삭제" @click="checkList('linkedAdvs', 'advs')"><img src="../../assets/images/icon/account_left.jpg" alt=""></button>
													<button type="button" title="추가" @click="checkList('advs', 'linkedAdvs')"><img src="../../assets/images/icon/account_right.jpg" alt=""></button>
												</div>
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
													<li v-for="(pixelMappingCategory, index) in pixelMappingCategories" :key="index" class="select_btn">
														<div class="select_title">{{ pixelMappingCategory.title }}</div>
														<div class="select_contents">
															<div><ui-select :selectData="pixelMappingCategory.select" :data-key="index" :onClick="multiSelect"></ui-select></div>
														</div>
													</li>
												</ul>
												<div class="btn_wrap">
													<button type="button" class="before_btn" @click="tabMove('1', '2')">이전</button>
													<button class="next_btn" @click="success()">완료</button>
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

		// 픽셀 맵핑 카테고리 목록
		this.$http.get('/pixel_mapping_category/')
		.then(res => {
			let categoryCount = res.data.count
			const data = res.data.data

			for(let i = 0; i < categoryCount; i++) {
				this.pixelMappingCategories.push({
					id: data[i].id,
					title: data[i].category_label_kr,
					number: i,
					key: i,
					select: {
						// select 속성이 없을때 childe vue의 selectData.default()가 호출 됨
						emptyText: this.defaultPixelEvent,
						textList: ['미지정']
					}
				})
			}

			return
		})
		// 픽셀 이벤트 목록
		.then(() => {
			this.$http.get('/fb_ad_accounts/ad_account_pixel_events', {
				//params: {fb_ad_account_id: localStorage.getItem('fb_ad_account_id')}
				params: {act_account_id: 'act_'+localStorage.getItem('account_id')}
			})
			.then(res => {
				const data = res.data.data

				this.pixelMappingCategories.forEach(category => {
					for(let i = 0; i < data.length; i++) {
						category.select.textList.push(data[i].name)
					}
				})
			})
		})
	},

	data () {
		return {
			tabActive1: true,
			tabActive2: false,
			tabActive3: false,
			tabListStep: 0,

			// 카테고리 설정
			categoryName: '',
			actAccountId: 0,
			accountCategoryId: 0,

			// 네오 계정 연동
			neoAdvIds: [],
			neoAccountIds: [],
			advs: [],
			linkedAdvs:[],
			checkedAdvs:[],
			searchKeyword: '',
			selected: [],
			addSelected:[],

			// 픽셀 이벤트 매핑
			facebookPixelEventNames: [],
			pixelMappingCategoryIds: [],
			pixelMappingCategories: [],
			defaultPixelEvent: '픽셀 이벤트를 선택해주세요.',
		}
	},

	methods:{
		clickSteop1Category (name) {
			this.categoryName = name
		},

		multiSelect (item, index) {
			// 해당 pixelMappingCategory의 pixelEvent를 변경하기 위함
			const key = event.target.closest('.select_btn').getAttribute('data-key')
			this.pixelMappingCategories[key].select.emptyText = item
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
			// (1) 카테고리 설정
			if (beforeNumber === '0') {
				if (this.categoryName === '') {
					alert('통계 및 계정 유형 분석을 선택해주세요.')
					return false
				} else {
					this.actAccountId = this.currentFbAdAccount.id

					if(this.categoryName === '대출') {
						this.accountCategoryId = 1
					} else if(this.categoryName === 'NGO') {
						this.accountCategoryId = 2
					} else if(this.categoryName === '카드') {
						this.accountCategoryId = 3
					} else if(this.categoryName === '여행') {
						this.accountCategoryId = 4
					} else if(this.categoryName === '쇼핑몰') {
						this.accountCategoryId = 5
					} else if(this.categoryName === '기타') {
						this.accountCategoryId = 6
					} else if(this.categoryName === '보험') {
						this.accountCategoryId = 7
					} else if(this.categoryName === '뷰티') {
						this.accountCategoryId = 8
					}
				}
			// (2) 네오 계정 연동
			} else if (activeNumber == '2' && beforeNumber === '1') {
				if(this.linkedAdvs.length == 0) {
					if(confirm('선택된 네오 계정이 없습니다. 계속 진행하시겠습니까?') === false) {
						return false
					}
				} else {
					// 추가된 네오 계정 리스트
					for(let i = 0; i < this.linkedAdvs.length; i++) {
						this.neoAdvIds.push(this.linkedAdvs[i].advertiserid)
						this.neoAccountIds.push(this.linkedAdvs[i].id)
					}
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
			// (3) 픽셀 이벤트 맵핑
			for(let i = 0; i < this.pixelMappingCategories.length; i++) {
				// 선택된 픽셀 이벤트
				let selectedPixelEvent = this.pixelMappingCategories[i].select.emptyText

				this.facebookPixelEventNames.push(selectedPixelEvent === '미지정' ? null : selectedPixelEvent)
				this.pixelMappingCategoryIds.push(this.pixelMappingCategories[i].id)
			}

			if(this.facebookPixelEventNames.includes(this.defaultPixelEvent)) {
				// 선택되지 않은 픽셀 이벤트가 있을 경우
				alert('모든 항목이 매칭되지 않았습니다.')
			} else {
				// 모든 픽셀 이벤트가 설정 되었을 경우
				if(confirm('현재 매칭된 상태로 Target Pick 설정을 진행할까요?') === true) {
					// 카테고리 설정 POST
					this.$http.post('/fb_ad_accounts/', {
							act_account_id: this.actAccountId,
							account_category_id: this.accountCategoryId,
					})
					.then(() => {
						// 네오 계정 연동 POST
						this.$http.post('/neo_account/', {
							fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
							neo_adv_ids: this.neoAdvIds,
							neo_account_ids: this.neoAccountIds
						})
						.then(() => {
							// 페이스북 광고 계정 정보 갱신
							this.$eventBus.$emit('getFbAdAccountInfo')
						})

						return
					})
					.then(() => {
						// 픽셀 이벤트 맵핑 POST
						this.$http.post('/pixel_mapping/', {
							fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
							facebook_pixel_event_names: this.facebookPixelEventNames,
							pixel_mapping_category_ids: this.pixelMappingCategoryIds,
						})

						return
					})
					.then(() => {
						this.neoAdvIds = []
						this.neoAccountIds = []
						this.facebookPixelEventNames = []
						this.pixelMappingCategoryIds = []

						// 페이스북 광고 계정 정보 갱신
						this.$eventBus.$emit('getFbAdAccountInfo')
						// 페이스북 광고 계정 설정창 닫기
						this.$emit('close')
					})
				} else {
					return false
				}
			}
		},
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
		currentFbAdAccount() {
			return this.$store.state.currentFbAdAccount
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

<style lang="css" scoped>
</style>
