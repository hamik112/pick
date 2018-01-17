<template>
	<div id="main_wrap" class="clearfix">
		<div id="container" v-show="isCreativeLibrary">
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div class="tab-contents-widget">
						<div id="section_list_3" class="section_tab_contents clearfix">
							<iframe id="creative-frame" :src="iframe.src" ref="frame" @load="load('creative-frame')" v-show="iframe.loaded" width="100%" :height="iframe.height" frameborder="0" allowfullscreen></iframe>
						</div>
					</div>
				</div>
			</div>
		</div>
		<ui-loading :isShow="isLoading" :titleText="loadingTitle" :descriptionText="loadingDescription"></ui-loading>
	</div>
</template>

<script>
//레이아웃 호출
import Loading from '@/components/ui/Loading'

export default {
	name: 'CreativeLibrary',

	components: {
		'ui-loading': Loading
	},

	mounted () {
		const me = this
		// Creative Library iframe 높이 값 받아오기
		window.addEventListener("message", receiveMessage, false);
		function receiveMessage(e) {
			me.iframe.height = e.data
		}
	},

	data () {
		return {
			iframe: {
				src: 'http://www.pickdata.co.kr:7777/creative/',
				height:0,
				loaded: false
			},
			isCreativeLibrary: true,
			isLoading: false,
			loadingTitle: 'Creative Library를 가져옵니다.',
			loadingDescription: '조금만 기다려 주시면 완료됩니다.'
		}
	},
	methods:{
		load: function(el){
			const me = this
			this.isCreativeLibrary = false
			this.isLoading = true

			this.iframe.loaded = true
			setTimeout(function() {
				me.isCreativeLibrary = true
				me.isLoading = false
			}, 2500)
		}
	}
}
</script>

<style lang="css" scoped>
</style>
