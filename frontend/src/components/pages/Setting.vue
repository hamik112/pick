<template>
	<div id="main_wrap" class="clearfix">
		<transition name='modal'>
			<advertising-account-setting v-if="popupStatus" @close="popupStatus = false"></advertising-account-setting>
		</transition>
		<div id="container">
			<div id="container_wrap">
				<div class="setting_contents_wrap">
					<div class="setting_wrap clearfix">
						<div class="user_info clearfix">
							<div class="u_logo"><img src="../../assets/images/common/test_img.jpg" alt=""></div>
							<div class="u_mask"></div>
							<div>
								<strong>{{ fbAdAccountName }}</strong>
								<p>계정번호 : {{ fbAdAccountAdAccountId }}</p>
							</div>
						</div>
						<div class="user_pixel">
							<p>사용 픽셀</p>
							<p>{{ fbAdAccountUsingCategory }}</p>
						</div>
						<div class="user_id">
							<p>연결된 네오 계정</p>
							<p>{{ fbAdAccountConnectedNeoAccountCount }}개</p>
						</div>
						<div class="user_event">
							<p>픽셀이벤트 매핑</p>
							<p>{{ fbAdAccountPixelEventMappingCount }}개</p>
						</div>
						<div class="setting_btn"><button type="button" @click="popupStatus = true">계정 설정 수정하기</button></div>
					</div>
					<div>※ 기존 픽셀 연결과 다르게 변경하실 경우,  픽데이터에서 생성 완료 한 타겟 사용이 어려울 수 있습니다.</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import AdvertisingAccountSetting from '@/components/popup/AdvertisingAccountSetting'

export default {
	name: 'Setting',
	
  components: {
		AdvertisingAccountSetting
	},
	
	created () {
		this.$eventBus.$on('getFbAdAccountInfo', this.getFbAdAccountInfo)
		this.getFbAdAccountInfo()
	},

	beforeDestroy () {
		this.$eventBus.$off('getFbAdAccountInfo', this.getFbAdAccountInfo)
	},

  data () {
    return {
			popupStatus: false,

			fbAdAccountName: '',
			fbAdAccountAdAccountId: '',
			fbAdAccountUsingCategory: '',
			fbAdAccountConnectedNeoAccountCount: 0,
			fbAdAccountPixelEventMappingCount: 0,
    }
	},

	methods: {
		getFbAdAccountInfo () {
			let fbAdAccountId = localStorage.getItem('fb_ad_account_id')
			
			const fbAdAccount = this.$store.state.currentFbAdAccount
			this.fbAdAccountName = fbAdAccount.name
			this.fbAdAccountAdAccountId = fbAdAccount.account_id

			if (fbAdAccountId === 'undefined') {
				this.fbAdAccountUsingCategory = '없음'
				this.fbAdAccountConnectedNeoAccountCount = 0
				this.fbAdAccountPixelEventMappingCount = 0
			} else {
				this.$http.get(`/fb_ad_accounts/${fbAdAccountId}`)
					.then(res => {
						const data = res.data

						this.fbAdAccountUsingCategory = data.account_category_name
						this.fbAdAccountConnectedNeoAccountCount = data.neo_account_count
						this.fbAdAccountPixelEventMappingCount = data.pixel_event_mapping_count
				})
				.catch(err => {
					console.log(err)
				})
			}
		}
	}
}
</script>

<style lang="css" scoped>
</style>
