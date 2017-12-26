<template>
	<div id="main_wrap" class="clearfix">
		<Header></Header>
		<div id="container">
			<Aside></Aside>
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div class="tab-contents-widget">
						<div id="section_list_3" class="section_tab_contents clearfix">크리에이티브 라이브러리</div>
					</div>
				</div>
			</div>
		</div>
		<Footer></Footer>
	</div>
</template>

<script>
	//레이아웃 호출
	import Header from '@/components/layout/Header'
	import Footer from '@/components/layout/Footer'
	import Aside from '@/components/layout/Aside'
	export default {

	  name: 'CreativeLibrary',
	  components: {'Header': Header,'Footer': Footer,'Aside': Aside},

	  data () {
	    return {

	    }
	  }
	}
</script>

<style lang="css" scoped>
</style>