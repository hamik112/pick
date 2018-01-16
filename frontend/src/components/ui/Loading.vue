<template>
	<div id="main_wrap" class="clearfix">
		<div id="container">
			<div id="container_wrap">
				<div id="section_list_4" class="section_tab_contents clearfix">
					<div class="loading_wrap">
						<!-- <div class="title">{{ titleMsg }}</div>
						<div class="prologue">{{ descriptionMsg }}</div> -->
						<div class="loading_chart">
							<div id="loading"></div>
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
	name: 'Loading',

	data () {
		return {
			titleMsg: '타겟을 최적화 하는 중입니다.',
			descriptionMsg: '조금만 기다려 주시면, 계정에 적합한 기본 타겟이 생성됩니다.'
		}
	}
}
</script>

<style lang="css" scoped>
</style>
