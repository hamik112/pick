<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="target_pop_01">
						<div class="popup-contents clearfix">
							<div class="pop_title_wrap">
								<div class="pop_title">타겟 만들기 (1/2)</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="pop_tab_wrap clearfix" v-if="tabActive1">
								<div class="cate_contents_widget">
									<ul class="target_pick_01">
										<li @click="tabMove(1)">
											<span>사이트방문</span>
										</li>
										<li @click="tabMove(1)">
											<span>특정페이지 방문</span>
										</li>
										<li @click="tabMove(1)">
											<span>NEO 타겟</span>
										</li>
										<li @click="tabMove(1)">
											<span>구글애널리틱스</span>
										</li>
									</ul>
									<ul class="target_pick_02">
										<li @click="tabMove(1)">
											<span>구매</span>
										</li>
										<li @click="tabMove(1)">
											<span>장바구니</span>
										</li>
										<li @click="tabMove(1)">
											<span>회원가입</span>
										</li>
										<li @click="tabMove(1)">
											<span>단계별 전환</span>
										</li>
									</ul>
								</div>
								<div class="btn_wrap">
									<button type="button" class="close_pop" @click="$emit('close')">취소</button>
								</div>
							</div>

							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabActive2">
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
													<div class="result_check"><input type="checkbox" id="target_type01"><label for="target_type01">매체</label></div>
												</li>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type02"><label for="target_type02">그룹</label></div>
												</li>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type03"><label for="target_type03">키워드</label></div>
												</li>
												<li>
													<div class="result_check"><input type="checkbox" id="target_type04"><label for="target_type04">엑셀업로드</label></div>
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
																<div class="result_list_inner">
																	<div class="result_thead">
																		<ul>
																			<li>
																				<div class="result_check"><input type="checkbox" id="all_check"><label for="all_check"></label></div>
																				<div class="result_account">계정명</div>
																				<div class="result_group">그룹명</div>
																				<div class="result_switch">전환 수</div>
																			</li>
																		</ul>
																	</div>
																	<div class="result_tbody">
																		<ul>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result01"><label for="target_result01"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result02"><label for="target_result02"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result03"><label for="target_result03"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result04"><label for="target_result04"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result05"><label for="target_result05"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result06"><label for="target_result06"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result07"><label for="target_result07"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result08"><label for="target_result08"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																			<li>
																				<div class="result_check"><input type="checkbox" id="target_result09"><label for="target_result09"></label></div>
																				<div class="result_account">LF몰</div>
																				<div class="result_group">LF_M_구글</div>
																				<div class="result_switch">LF_M_구글</div>
																			</li>
																		</ul>
																	</div>
																</div>
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

// UI
import Select from '@/components/ui/Select'

export default {

  name: 'TargetMake01',
  components:{
  	'ui-select': Select
  },
  data () {
    return {
    	tabActive1:true,
    	tabActive2:false,
    	categoryName:'',

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
	tabMove(activeNumber, beforeNumber) {
		let tabArray = ['tabActive1','tabActive2']
		for(let i = 0; i < tabArray.length; i++) {
			if(i == activeNumber) {
				this[tabArray[i]] = true
			}else{
				this[tabArray[i]] = false
			}
		}
	},
	selectTarget: function (item) {
		this.selectData.emptyText = item
	}
  }
}
</script>

<style lang="css" scoped>
</style>
