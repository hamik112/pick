<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="target_pop_01">
						<div class="popup-contents clearfix">
							<div class="pop_title">타겟 만들기 (1/2)</div>
							<div class="pop_tab_wrap clearboth">
								<div class="cate_contents_widget">
									<ul class="target_pick_01">
										<li>
											<span>사이트방문</span>
										</li>
										<li>
											<span>특정페이지 방문</span>
										</li>
										<li>
											<span>NEO 타겟</span>
										</li>
										<li>
											<span>구글애널리틱스</span>
										</li>
									</ul>
									<ul class="target_pick_02">
										<li>
											<span>구매</span>
										</li>
										<li>
											<span>장바구니</span>
										</li>
										<li>
											<span>회원가입</span>
										</li>
										<li>
											<span>단계별 전환</span>
										</li>
									</ul>
								</div>
								<div class="btn_wrap">
									<button type="button" class="close_pop" @click="$emit('close')">취소</button>
								</div>
							</div>
							<p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')">X</button></p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
export default {

  name: 'TargetMake01',

  data () {
    return {

    }
  }
}
</script>

<style lang="css" scoped>
</style>
