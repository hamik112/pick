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
	    	console.log(this.getDocHeight(el))
	    },
	    getDocHeight(doc) {
		    doc = doc || document;
		    let body = doc.body
		    let html = doc.documentElement
		    let height = Math.max( body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight )
		    return height;
		}
	  }
	}
</script>

<style lang="css" scoped>
</style>
