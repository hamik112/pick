<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="ad_set_pop_1">
						<div class="popup-contents">
							<div class="pop_title_wrap">
								<!-- 타이틀 -->
								<div class="pop_title">광고계정 설정하기</div>
								<!-- 팝업 닫기 -->
								<p class="popup-btn">
									<button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')">
										<img src="../../assets/images/target/white_close_i.png" alt="">
									</button>
								</p>
							</div>
							<!-- 광고 계정 정보 -->
							<div class="ad_info_wrap">
								<div class="ad_mask"></div>
								<div class="ad_image">
									<img src="../../assets/images/common/test_img.jpg" alt="">
								</div>
								<div class="ad_info">
									<strong>{{ this.currentFbAdAccount.name }}</strong>
									<div>계정번호:{{ this.currentFbAdAccount.account_id }}</div>
								</div>
							</div>
							<!-- 광고 계정 설정-->
							<div class="list-tab-widget">
								<!-- 네비게이터 -->
								<div class="tab-nav-widget">
									<ul>
										<li rel="tab-list-1" v-bind:class="[currentStep === 0 ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>1</span>카테고리 설정</a>
										</li>
										<li rel="tab-list-2" v-bind:class="[currentStep === 1 ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>2</span>네오 계정 연동</a>
										</li>
										<li rel="tab-list-3" v-bind:class="[currentStep === 2 ? 'active' : '']">
											<p></p>
											<a href="javascript:void(0);"><span>3</span>픽셀 이벤트 매핑</a>
										</li>
									</ul>
								</div>
								<!-- 광고계정 설정 프로세스 -->
								<div class="pop_tab_wrap">
									<div class="tab-contents-widget" >
										<!-- Step1: 카테고리 설정 -->
										<category-setting v-show="isActive[0]"
											@setCategory="setCategory">
										</category-setting>
										<!-- Step2: 네오 계정 연동 -->
										<neo-account-linkage v-show="isActive[1]"
											@backToSetCategory="backToSetCategory"
											@setNeoAccountLinkage="setNeoAccountLinkage">
										</neo-account-linkage>
										<!-- Step3: 픽셀 이벤트 맵핑 -->
										<pixel-event-mapping v-show="isActive[2]"
											@backToNeoAccountLinkage="backToNeoAccountLinkage"
											@setPixelEventMapping="setPixelEventMapping"
											:emptyTextId="emptyTextId">
										</pixel-event-mapping>
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
import CategorySetting from '@/components/popup/setting/CategorySetting'
import NeoAccountLinkage from '@/components/popup/setting/NeoAccountLinkage'
import PixelEventMapping from '@/components/popup/setting/PixelEventMapping'

export default {
	components: {
		CategorySetting,
		NeoAccountLinkage,
		PixelEventMapping
	},

	data () {
		return {
			currentStep: 0,
			isActive: [true, false, false],

			actAccountId: 0,

			accountCategoryId: 0,
			emptyTextId: 0,
			neoAdvIds: [],
			neoAccountIds: [],
			facebookPixelEventNames: [],
			pixelMappingCategoryIds: []
		}
	},

	computed: {
		currentFbAdAccount() {
			return this.$store.state.currentFbAdAccount
		}
	},

	methods: {
		// 카테고리 설정 ------------------------------------------------
		setCategory (steps, accountCategoryId, emptyTextId) {
			this.currentStep = 1
			this.isActive = steps
			this.accountCategoryId = accountCategoryId
			this.emptyTextId = emptyTextId
		},


		// 네오 계정 연동 -----------------------------------------------
		backToSetCategory (steps) {
			this.currentStep = 0
			this.isActive = steps
		},

		setNeoAccountLinkage (steps, neoAdvIds, neoAccountIds) {
			this.currentStep = 2
			this.isActive = steps
			this.neoAdvIds = neoAdvIds
			this.neoAccountIds = neoAccountIds
		},


		// 픽셀 이벤트 맵핑 ----------------------------------------------
		backToNeoAccountLinkage (steps) {
			this.currentStep = 1
			this.isActive = steps
		},

		setPixelEventMapping (facebookPixelEventNames, pixelMappingCategoryIds) {
			this.facebookPixelEventNames = facebookPixelEventNames
			this.pixelMappingCategoryIds = pixelMappingCategoryIds

			// 카테고리 설정 POST
			this.$http.post('/fb_ad_accounts/', {
				act_account_id: this.currentFbAdAccount.id,
				account_category_id: this.accountCategoryId,
				pixel_id: this.emptyTextId,
			})
			.then(res => {
				const response = res.data
				const data = response.data
				const success = response.success
				if (success === "YES") {
					localStorage.setItem('fb_ad_account_id', data.id)
				}

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
			})
			.then(() => {
				// 픽셀 이벤트 맵핑 POST
				this.$http.post('/pixel_mapping/', {
					fb_ad_account_id: localStorage.getItem('fb_ad_account_id'),
					facebook_pixel_event_names: this.facebookPixelEventNames,
					pixel_mapping_category_ids: this.pixelMappingCategoryIds,
				})
				.then(res => {

				})
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
		}
	}
}
</script>

<style lang="css" scoped>
</style>
