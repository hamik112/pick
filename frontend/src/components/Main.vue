<template>
<div id="main_wrap" class="clearfix">
	<Header></Header>
	<div id="container">
		<Aside></Aside>
		<div id="container_wrap">
			메인
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
	//팝업
	import AdSetPop from '@/components/popup/Advertising_setup'
	import TargetChartPop from '@/components/popup/Target_chart'
	import TargetMake01 from '@/components/popup/Target_make_01'
	import TargetMake02 from '@/components/popup/Target_make_02'


	export default {
	  name: 'Main',
	  components: {'Header': Header,'Footer': Footer,'Aside': Aside},
	  data () {
	    return {
	      data: false
	    }
	  }
	}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
