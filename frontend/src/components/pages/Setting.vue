<template>
	<div id="main_wrap" class="clearfix">

		<transition name='modal'>
			<SetupPop v-if="setPop" @close="setPop = false"></SetupPop>
		</transition>

		<div id="container">
			<div id="container_wrap">
				<div class="setting_contents_wrap">
					<div class="setting_wrap clearfix">
						<div class="user_info clearfix">
							<div class="u_logo"><img src="../../assets/images/common/test_img.jpg" alt=""></div>
							<div class="u_mask"></div>
							<div>
								<strong>프리메라프리메라</strong>
								<p>계정번호 : 1051325123890</p>
							</div>
						</div>
						<div class="user_pixel">
							<p>사용 픽셀</p>
							<p>금융</p>
						</div>
						<div class="user_id">
							<p>연결된 네오 계정</p>
							<p>3개</p>
						</div>
						<div class="user_event">
							<p>픽셀이벤트 매핑</p>
							<p>5개</p>
						</div>
						<div class="setting_btn"><button type="button" @click="setPop = true">계정 설정 수정하기</button></div>
					</div>
					<div>※ 기존 픽셀 연결과 다르게 변경하실 경우,  픽데이터에서 생성 완료 한 타겟 사용이 어려울 수 있습니다.</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

import SetupPop from '@/components/popup/Advertising_setup'

export default {

  name: 'Setting',
  components:{
  	SetupPop:SetupPop
  },

  data () {
    return {
    	setPop:false
    }
  }
}
</script>

<style lang="css" scoped>
</style>
