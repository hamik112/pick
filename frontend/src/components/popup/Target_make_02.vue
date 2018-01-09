<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget pop-scroll" id="target_pop_02">
						<div class="popup-contents clearfix">
							<div class="pop_title_wrap">
								<div class="pop_title">타겟 만들기 (2/2)</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close-btn close_pop" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="target_contents_wrap clearfix">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/neo_logo.png" alt="neo"></div>
											<div class="title_info">
												<p>NEO타겟</p>
												<p>타겟의 속성을 정의하세요</p>
											</div>
										</div>
										<div class="use_wrap">
											<div class="use_select">
												<div class="contents_title">사용픽셀</div>
												<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
											</div>
											<div class="use_date">
												<div>수집기간 : 최근</div>
												<div><input type="text"><span>일</span></div>
											</div>
										</div>
										<div class="target_name">
											<div class="contents_title">타겟이름</div>
											<div><input type="text"></div>
										</div>
										<div class="target_data">
											<div class="contents_title">타겟 모수</div>
											<div>
												<span>12,000</span>명
											</div>
										</div>
										<div class="target_type">
											<div class="contents_title">Neo 유형</div>
											<ul>
												<li>
													<div class="result_check"><input type="radio" id="target_type01"><label for="target_type01">매체</label></div>
												</li>
												<li>
													<div class="result_check"><input type="radio" id="target_type02"><label for="target_type02">그룹</label></div>
												</li>
												<li>
													<div class="result_check"><input type="radio" id="target_type03"><label for="target_type03">키워드</label></div>
												</li>
												<li>
													<div class="result_check"><input type="radio" id="target_type04"><label for="target_type04">엑셀업로드</label></div>
												</li>
											</ul>
										</div>
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="cate_contents">
												<div class="account_info">
													<div class="account_title">"아래 그룹로 유입된 사람"중</div>
													<div>
														<ui-select :selectData="this.selectData2" :onClick="selectTarget"></ui-select>
													</div>
													<div class="account_date">
														<input type="text"><span>일</span>
													</div>
												</div>
												<div class="account_wrap">
													<div class="account_inner_wrap clearfix">
														<div class="account_left">
															<div class="advertiser_search_result pop-scroll">

															</div>
															<div class="account_add_wrap">
																<div>*최근 한달 기준</div>
																<button>선택한 매체 추가</button>
															</div>
														</div>
														<div class="account_right clearfix">
															<button><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
															<ul>
																<li class="sticker_btn">
																	<span>모바일 DA_페이스북 (질바이질슈즈)</span>
																</li>
																<li class="sticker_btn">
																	<span>모바일 DA_페이스북 (질바이질슈즈)</span>
																</li>
																<li class="sticker_btn">
																	<span>모바일 DA_페이스북 (질바이질슈즈)</span>
																</li>
															</ul>
														</div>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="$emit('close')">취소</button>
									<button class="delete_btn">타겟 삭제</button>
									<button class="adjust_btn">타겟 수정</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
//UI Components Files
import { Select, Calendar, Charts } from '@/components/componentsUI.js'

export default {
  name: 'TargetMake02',
  components:{
  	'ui-select': Select
  },
  data () {
    return {
    	selectData: {
          emptyText: '전체보기',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        },
        selectData2: {
          emptyText: '특정일 동안 미방문 고객',
          textList: [
            '이벤트1',
            '이벤트2',
            '이벤트3'
          ]
        }
    }
  },
	methods: {
		selectTarget: function (item) {
			this.selectData.emptyText = item
		}
	}
}
</script>
