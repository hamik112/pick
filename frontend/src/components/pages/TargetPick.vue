<template>
	<div id="main_wrap" class="clearfix">

		<transition name='modal'>
			<TargetChartPop v-if="chartModal" @close="chartModal = false"></TargetChartPop>
			<TargetMake1 v-if="makeModal1" @close="makeModal1 = false"></TargetMake1>
		</transition>

		<transition-group name='modal'>
			<SetupPop v-if="setupPop" @close="setupPop = false" key="setup"></SetupPop>
			<PixelNone v-if="pixelNone" @close="pixelNone = false" key="pixel"></PixelNone>
		</transition-group>

		<div id="container">
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div class="tab-contents-widget">
						<div id="section_list_1" class="section_tab_contents clearfix">
							<div class="target_aside">
								<ul>
									<li class="on">전체<span>{{ targetCount.totalCount }}</span></li>
									<li>사이트방문<span>{{ targetCount.visitPagesCount }}</span></li>
									<li>특정페이지 방문<span>{{ targetCount.visitSpecificPagesCount }}</span></li>
									<li>NEO 타겟<span>{{ targetCount.neoTargetCount }}</span></li>
									<li>UTM 티켓<span>{{ targetCount.utmTargetCount }}</span></li>
									<li>구매<span>{{ targetCount.purchaseCount }}</span></li>
									<li>장바구니<span>{{ targetCount.addToCartCount }}</span></li>
									<li>회원가입<span>{{ targetCount.registrationCount }}</span></li>
									<li>단계별전환<span>{{ targetCount.conversionCount }}</span></li>
								</ul>
							</div>
							<div class="target_contents_wrap">
								<div class="target_setup">
									<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
									<button type="button" @click="makeModal1 = true">타겟만들기</button>
								</div>
								<div class="target_contents">
									<ul>
										<li v-for="item in this.targetList.total" @click="chartModal = true">
											<div class="target_icon">
												<div class="icon_target" v-bind:class="[(item.targeting_complete) ? 'on' : '']"></div>
												<div class="icon_gragh" v-bind:class="[(item.demographic_complete) ? 'on' : '']"></div>
											</div>
											<div class="target_info">
												<p>{{ item.name }}</p>
												<p>{{ item.display_count }}</p>
											</div>
											<div class="target_state">
												<p>{{ item.description.pixel_mapping_category }}</p>
												<p>{{ item.description.retention_days }}일</p>
												<p>{{ item.description.description }}</p>
												<p v-if="item.description.option != ''">{{ item.description.option }}</p>
											</div>
										</li>
										<li class="target_last"><a href="javascript:void(0);" @click="makeModal1 = true"><img src="../../assets/images/common/target_add.jpg" alt=""></a></li>
									</ul>
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
	// 팝업
	import TargetChartPop from '@/components/popup/Target_chart'
	import TargetMake1 from '@/components/popup/Target_make_01'
	// UI
	import Select from '@/components/ui/Select'
	import Calendar from '@/components/ui/Calendar'

	import SetupPop from '@/components/popup/Advertising_setup'
	import PixelNone from '@/components/popup/Target_not_available'

	export default {
		name: 'TargetPick',

		components: {
			'TargetChartPop': TargetChartPop,
			'TargetMake1': TargetMake1,
			'ui-select': Select,
			'ui-calendar': Calendar,
			'SetupPop': SetupPop,
			'PixelNone': PixelNone
		},

		data () {
			return {
				setupPop: false,
				pixelNone: false,
				chartModal: false,
				makeModal1: false,
				makeModal2: false,
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
				}
			}
		},

		computed: {
			computedIconTargetClass (item) {
				console.log(item)
				return this.itemObject.iconTargetClass
			}
		},

		created () {
			this.$eventBus.$on('selectFbAdAccount', this.selectFbAdAccount)
		},

		methods: {
			selectTarget (item) {
				this.selectData.emptyText = item
			},

			selectFbAdAccount (fbAdAccount) {
				console.log('selectFbAdAccount', fbAdAccount)
				this.checkFbAdAccount(fbAdAccount)
				this.getAccountTarget(fbAdAccount)
			},

			checkFbAdAccount (fbAdAccount) {
				console.log('checkFbAdAccount', fbAdAccount)
				const account_id = fbAdAccount.account_id
				let url = '/api/fb_ad_accounts/confirm_ad_account?act_account_id=act_' + account_id
				this.$http.get(url)
				.then(res => {
					const bool_default_pixel = res.data.bool_default_pixel
					const bool_fb_ad_account = res.data.bool_fb_ad_account
					if (bool_fb_ad_account == false) {
            // Advertising_setup popup 호출
						this.setupPop = true
					} else {
						this.setupPop = false
					}
					if (bool_default_pixel == false) {
            // default_pixel alert popup
						this.pixelNone = true
					} else {
						this.pixelNone = false
					}
				})
			},

			getAccountTarget (fbAdAccount) {
				console.log('getAccountTarget', fbAdAccount)
				let url = '/api/pickdata_account_target/targetpick?fb_ad_account_id=2'
				this.$http.get(url)
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
					} else {
						throw('success: ' + success)
					}
				})
				.catch(err => {
					console.error('/api/pickdata_account_target/targetpick', err)
				})
			}
		}
	}
</script>

<style lang="css" scoped>
</style>
