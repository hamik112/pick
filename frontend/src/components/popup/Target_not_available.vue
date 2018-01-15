<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="target_not">
						<div class="popup-contents clearfix">
							<div class="pop_title_wrap">
								<div class="pop_title"></div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close-btn close_pop" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="target_chart_graph_wrap">
								<div class="title">Not Available</div>
									<div class="prologue">
										<p>해당 비즈니스 계정이 보유하고 있는 픽셀이 없습니다.</p>
										<p>페이스북에서 픽셀을 설정해 주세요.</p>
									</div>
								<div class="chart_close_btn close_pop" @click="$emit('close')">확인</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
// UI
export default {

  name: 'TargetNot',
  components:{
  },
  data () {
	return {
	}
  }
}
</script>

<style lang="css" scoped>
</style>
