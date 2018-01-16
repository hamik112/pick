<template>
	<div id="main_wrap" class="clearfix">
		<div id="container">
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
	</div>
</template>

<script>
//레이아웃 호출
export default {
	name: 'CreativeLibrary',
	mounted () {
		let me = this
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
			}
		}
	},
	methods:{
		load: function(el){
			this.iframe.loaded = true;
			this.iframe.height = window.innerHeight
			setTimeout(function() {
				document.getElementById(el).style = 'display: block'
			}, 1000)
		}
	}
}
</script>

<style lang="css" scoped>
#creative-frame { display: none; }
</style>
