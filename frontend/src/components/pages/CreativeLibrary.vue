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
	//UI Components Files
	import { Header, Footer, Aside, TargetChartPop, TargetMake1, TargetMake2, Select, Calendar } from '@/components/componentsUI.js'

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