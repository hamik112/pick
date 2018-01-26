<template>
	<div id="main_wrap" class="clearfix" >

		<transition name='modal'>
			<target-chart v-if="chartModal" @close="chartModal = false"></target-chart>
			<create-target v-if="makeModal" :makeType="this.makeType" :makeItem="this.makeItem" @close="makeModal = false"></create-target>
		</transition>

		<transition-group name='modal'>
			<advertising-account-setting v-if="setupPop" @close="setupPop = false" key="setup"></advertising-account-setting>
			<not-available v-if="pixelNone" @close="pixelNone = false" key="pixel"></not-available>
		</transition-group>

		<div id="container" v-show="isPick">
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div class="tab-contents-widget">
						<div id="section_list_1" class="section_tab_contents clearfix">
							<div class="target_aside">
								<ul id="target_aside_ul">
									<li><a id="p-menu0" href="javascript:void(0)" @click="tPickMenu('total')" :class="[(this.targetOn == 'total') ? 'on' : '']">전체<span>{{ targetCount.totalCount }}</span></a></li>
									<li><a id="p-menu1" href="javascript:void(0)" @click="tPickMenu('visitPages')" :class="[(this.targetOn == 'visitPages') ? 'on' : '']">사이트방문<span>{{ targetCount.visitPagesCount }}</span></a></li>
									<li><a id="p-menu2" href="javascript:void(0)" @click="tPickMenu('visitSpecificPages')" :class="[(this.targetOn == 'visitSpecificPages') ? 'on' : '']">특정페이지 방문<span>{{ targetCount.visitSpecificPagesCount }}</span></a></li>
									<li><a id="p-menu3" href="javascript:void(0)" @click="tPickMenu('neoTarget')" :class="[(this.targetOn == 'neoTarget') ? 'on' : '']">NEO 타겟<span>{{ targetCount.neoTargetCount }}</span></a></li>
									<li><a id="p-menu4" href="javascript:void(0)" @click="tPickMenu('utmTarget')" :class="[(this.targetOn == 'utmTarget') ? 'on' : '']">구글애널리틱스<span>{{ targetCount.utmTargetCount }}</span></a></li>
									<li><a id="p-menu5" href="javascript:void(0)" @click="tPickMenu('purchase')" :class="[(this.targetOn == 'purchase') ? 'on' : '']">구매<span>{{ targetCount.purchaseCount }}</span></a></li>
									<li><a id="p-menu6" href="javascript:void(0)" @click="tPickMenu('addToCart')" :class="[(this.targetOn == 'addToCart') ? 'on' : '']">장바구니<span>{{ targetCount.addToCartCount }}</span></a></li>
									<li><a id="p-menu7" href="javascript:void(0)" @click="tPickMenu('registration')" :class="[(this.targetOn == 'registration') ? 'on' : '']">회원가입<span>{{ targetCount.registrationCount }}</span></a></li>
									<li><a id="p-menu8" href="javascript:void(0)" @click="tPickMenu('conversion')" :class="[(this.targetOn == 'conversion') ? 'on' : '']">단계별전환<span>{{ targetCount.conversionCount }}</span></a></li>
								</ul>
							</div>
							<div class="target_contents_wrap">
								<div class="target_setup">
									<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
									<button type="button" @click="popupOpenBtn('makeModal','add')">타겟만들기</button>
								</div>
								<div class="target_contents">
									<ul>
										<li v-for="(item, index) in this.targetList[this.targetOn]" :key="index">
											<div class="target_icon">
												<!-- <div class="icon_target" v-bind:class="[(item.targeting_complete) ? 'on' : '']" @click="makeModal1 = true"></div>
												<div class="icon_gragh" v-bind:class="[(item.demographic_complete) ? 'on' : '']" @click="chartModal = true"></div> -->
												<div class="icon_target" @click="popupOpenBtn('makeModal','modify', item)"></div>
												<div class="icon_gragh" @click="chartModal = true"></div>
												<button type="button" @click="popupOpenBtn('makeModal','modify', item)">수정</button>
											</div>
											<div class="target_info">
												<p>{{ item.name }}</p>
												<p><span class="opensans">{{ item.display_count }}</span></p>
											</div>
											<div class="target_state">
												<p>{{ item.description.pixel_mapping_category }}</p>
												<p>{{ item.description.retention_days }}일</p>
												<p>{{ item.description.description }}</p>
												<p v-if="item.description.option != ''">{{ item.description.option }}</p>
											</div>
										</li>
										<li class="target_last"><a href="javascript:void(0);" @click="popupOpenBtn('makeModal','add')"><img src="../../assets/images/common/target_add.jpg" alt=""></a></li>
									</ul>
								</div>

							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<ui-loading :isShow="isLoading" :titleText="loadingTitle" :descriptionText="loadingDescription"></ui-loading>
	</div>
</template>

<script>
	// Popup
	import TargetChart from '@/components/popup/TargetChart'
	import CreateTarget from '@/components/popup/CreateTarget'
	import AdvertisingAccountSetting from '@/components/popup/AdvertisingAccountSetting'
	import NotAvailable from '@/components/popup/NotAvailable'

	// UI
	import Select from '@/components/ui/Select'
	import Calendar from '@/components/ui/Calendar'
	import Loading from '@/components/ui/Loading'

	export default {
		name: 'TargetPick',

		components: {
			TargetChart,
			CreateTarget,
			AdvertisingAccountSetting,
			NotAvailable,
			'ui-select': Select,
			'ui-calendar': Calendar,
			'ui-loading': Loading,
		},

		data () {
			return {
				setupPop: false,
				pixelNone: false,
				chartModal: false,
				makeModal: false,
				makeType:'add',
				makeItem: {},

				targetOn:'total',

				selectData: {
					emptyText: '전체보기',
					textList: [
						'전체보기',
						'기본 타겟만 보기',
						'생성 타겟만 보기',
						'타겟팅 완료된 타겟만 보기',
						'타겟팅 진행중인 타겟만 보기',
						'인구통계데이터가 있는 타겟만 보기'
					]
				},

				itemObject: {
					iconTargetClass: {
						iconTarget: true,
						on: false
					}
				},

				targetList: {
					total: [],
					registration: [],
					conversion: [],
					addToCart: [],
					visitSpecificPages: [],
					visitPages: [],
					utmTarget: [],
					purchase: [],
					neoTarget: []
				},

				targetCount: {
					totalCount: 0,
					registrationCount: 0,
					conversionCount: 0,
					addToCartCount: 0,
					visitSpecificPagesCount: 0,
					visitPagesCount: 0,
					utmTargetCount: 0,
					purchaseCount: 0,
					neoTargetCount: 0
				},

				isPick: false,
				isLoading: false,
				loadingTitle: '',
				loadingDescription: ''

			}
		},

		computed: {
			computedIconTargetClass (item) {
				console.log(item)
				return this.itemObject.iconTargetClass
			}
		},

		created () {
			this.$eventBus.$on('getTargetPick', this.getTargetPick)
			this.$eventBus.$on('getAccountTarget', this.getAccountTarget)
			const fbAdAccount = this.$store.state.currentFbAdAccount
			if (fbAdAccount !== '') {
				this.getTargetPick(fbAdAccount)
			}
		},

		beforeDestroy () {
		    this.$eventBus.$off('getTargetPick', this.getTargetPick)
				this.$eventBus.$off('getAccountTarget', this.getAccountTarget)
		},

		methods: {
			selectTarget (item) {
				console.log(item)
				let target_type = ""

				if (item == "전체보기") {
					target_type="all"
				} else if (item == "전체보기") {
					target_type="all"
				} else if (item == "기본 타겟만 보기") {
					target_type="default"
				} else if (item == "생성 타겟만 보기") {
					target_type="created"
				} else if (item == "타겟팅 완료된 타겟만 보기") {
					target_type="targeting_completed"
				} else if (item == "타겟팅 진행중인 타겟만 보기") {
					target_type="targeting_progress"
				} else if (item == "인구통계데이터가 있는 타겟만 보기") {
					target_type="demographic"
				} else {
					target_type="all"
				}

				this.isPick = false
				this.isLoading = true
				this.loadingTitle = '타겟을 가져오는 중입니다.'
				this.loadingDescription = '조금만 기다려 주시면, 생성된 타겟을 가져옵니다.'

				let url = '/pickdata_account_target/targetpick'
				this.$http.get(url, {
					params: {
						fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
						target_type: target_type
					}
				})
				.then(res => {
					const response = res.data
					const data = response.data
					const success = response.success
					if (success === "YES") {
						const total = data.total.data
						const visitPages = data['visit pages'].data
						const visitSpecificPages = data['visit specific pages'].data
						const neoTarget = data['neo target'].data
						const utmTarget = data['utm target'].data
						const purchase = data.purchase.data
						const addToCart = data['add to cart'].data
						const registration = data.registration.data
						const conversion = data.conversion.data

						const totalCount = data.total.count
						const visitPagesCount = data['visit pages'].count
						const visitSpecificPagesCount = data['visit specific pages'].count
						const neoTargetCount = data['neo target'].count
						const utmTargetCount = data['utm target'].count
						const purchaseCount = data.purchase.count
						const addToCartCount = data['add to cart'].count
						const registrationCount = data.registration.count
						const conversionCount = data.conversion.count

						this.targetList.total = total
						this.targetList.visitPages = visitPages
						this.targetList.visitSpecificPages = visitSpecificPages
						this.targetList.neoTarget = neoTarget
						this.targetList.utmTarget = utmTarget
						this.targetList.purchase = purchase
						this.targetList.addToCart = addToCart
						this.targetList.registration = registration
						this.targetList.conversion = conversion

						this.targetCount.totalCount = totalCount
						this.targetCount.visitPagesCount = visitPagesCount
						this.targetCount.visitSpecificPagesCount = visitSpecificPagesCount
						this.targetCount.neoTargetCount = neoTargetCount
						this.targetCount.utmTargetCount = utmTargetCount
						this.targetCount.purchaseCount = purchaseCount
						this.targetCount.addToCartCount = addToCartCount
						this.targetCount.registrationCount = registrationCount
						this.targetCount.conversionCount = conversionCount

						console.log(addToCart)
						this.isPick = true
						this.isLoading = false
					} else {
						throw('success: ' + success)
						this.isPick = true
						this.isLoading = false
					}
				})
				.catch(err => {
					//this.isPick = true
					this.isLoading = false
					console.error('/pickdata_account_target/targetpick', err)
				})


				this.selectData.emptyText = item
			},
			popupOpenBtn (popupName, type, item) {
				//팝업 오픈
				//popupName = 팝업컴포넌트명, type = add,modify,delete
				this[popupName] = true
				if(popupName === 'makeModal') {
					if (type === 'modify') {
						this.makeItem = item
					}
					this.makeType = type
				}
			},
			tPickMenu (type) {
				//매뉴 온오프 or 리스트 필터
				this.targetOn = type
			},
			getTargetPick (fbAdAccount) {
				this.isPick = false
				this.isLoading = true
				this.loadingTitle = '광고계정을 검사중입니다.'
				this.loadingDescription = '조금만 기다려 주시면, 확인이 완료됩니다.'

				const account_id = fbAdAccount.account_id
				let url = '/fb_ad_accounts/confirm_ad_account?act_account_id=act_' + account_id
				this.$http.get(url)
				.then(res => {
					const bool_default_pixel = res.data.bool_default_pixel
					const bool_fb_ad_account = res.data.bool_fb_ad_account

					if (bool_default_pixel == false) {
            // default_pixel alert popup
						this.pixelNone = true
						this.isPick = false
					} else {
						this.pixelNone = false

						if (bool_fb_ad_account == false) {
							// AdvertisingAccountSetting popup 호출
							this.isPick = false
							this.setupPop = true
							this.isLoading = false
						} else {
							this.setupPop = false
							this.isLoading = false
							//this.isPick = true

							localStorage.setItem('fb_ad_account_id', res.data.fb_ad_account.fb_ad_account_id)
							this.getAccountTarget(fbAdAccount)
						}
					}

					//this.isPick = true
					//this.isLoading = false

				})
				.catch(err => {
					//this.isPick = true
					this.isLoading = false
					console.error('/pickdata_account_target/targetpick', err)
				})
			},

			getAccountTarget (fbAdAccount) {
				// console.log('getAccountTarget', fbAdAccount)
				this.isPick = false
				this.isLoading = true
				this.loadingTitle = '타겟을 가져오는 중입니다.'
				this.loadingDescription = '조금만 기다려 주시면, 생성된 타겟을 가져옵니다.'

				let url = '/pickdata_account_target/targetpick'
				this.$http.get(url, {
					params: {
						fb_ad_account_id: localStorage.getItem('fb_ad_account_id')
					}
				})
				.then(res => {
					const response = res.data
					const data = response.data
					const success = response.success
					if (success === "YES") {
						const total = data.total.data
						const visitPages = data['visit pages'].data
						const visitSpecificPages = data['visit specific pages'].data
						const neoTarget = data['neo target'].data
						const utmTarget = data['utm target'].data
						const purchase = data.purchase.data
						const addToCart = data['add to cart'].data
						const registration = data.registration.data
						const conversion = data.conversion.data

						const totalCount = data.total.count
						const visitPagesCount = data['visit pages'].count
						const visitSpecificPagesCount = data['visit specific pages'].count
						const neoTargetCount = data['neo target'].count
						const utmTargetCount = data['utm target'].count
						const purchaseCount = data.purchase.count
						const addToCartCount = data['add to cart'].count
						const registrationCount = data.registration.count
						const conversionCount = data.conversion.count

						this.targetList.total = total
						this.targetList.visitPages = visitPages
						this.targetList.visitSpecificPages = visitSpecificPages
						this.targetList.neoTarget = neoTarget
						this.targetList.utmTarget = utmTarget
						this.targetList.purchase = purchase
						this.targetList.addToCart = addToCart
						this.targetList.registration = registration
						this.targetList.conversion = conversion

						this.targetCount.totalCount = totalCount
						this.targetCount.visitPagesCount = visitPagesCount
						this.targetCount.visitSpecificPagesCount = visitSpecificPagesCount
						this.targetCount.neoTargetCount = neoTargetCount
						this.targetCount.utmTargetCount = utmTargetCount
						this.targetCount.purchaseCount = purchaseCount
						this.targetCount.addToCartCount = addToCartCount
						this.targetCount.registrationCount = registrationCount
						this.targetCount.conversionCount = conversionCount

						console.log(addToCart)
						this.isPick = true
						this.isLoading = false
					} else {
						throw('success: ' + success)
						this.isPick = true
						this.isLoading = false
					}
				})
				.catch(err => {
					this.isPick = true
					this.isLoading = false
					console.error('/pickdata_account_target/targetpick', err)
				})
			}
		}
	}
</script>

<style lang="css" scoped>
</style>
