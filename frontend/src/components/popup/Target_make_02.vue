<template>
	<div class="layer-pop-widget">
		<div class="pop-bg" onclick="layerClose(this ,false);"></div>
		<div class="popup-widget" id="target_pop_02">
			<div class="popup-contents">
				<div class="pop_title">타겟 만들기 (2/2)</div>
				<div class="target_contents_wrap clearfix">
					<div>
						<div class="target_thead">
							<div class="main_title">
								<div><img src="images/target/neo_logo.png" alt="neo"></div>
								<div class="title_info">
									<p>NEO타겟</p>
									<p>타겟의 속성을 정의하세요</p>
								</div>
							</div>
							<div class="use_wrap">
								<div class="use_select">
									<div class="contents_title">사용픽셀</div>
									<div class="select_btn">
										<div class="select_contents">
											<div class="select"><p>픽셀 이벤트를 선택해주세요</p></div>
											<ul class="select_view">
												<li>12346</li>
												<li>이벤43573457트2</li>
												<li>34574a</li>
											</ul>
										</div>
									</div>
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
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>특정일 동안 미방문 고객</p></div>
													<ul class="select_view">
														<li>이벤트1</li>
														<li>이벤트2</li>
														<li>이벤트3</li>
													</ul>
												</div>
											</div>
										</div>
										<div class="account_date">
											<input type="text"><span>일</span>
										</div>
									</div>
									<div class="account_wrap">
										<div class="account_inner_wrap clearfix">
											<div class="account_left">
												<div class="advertiser_search_result pop-scroll">
													<div>
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
												<button><img src="images/target/target_close_btn.png" alt=""></button>
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
								<!-- 엑셀 업로드-->
								<!-- <div class="cate_contents target_excel">
									<div class="account_info">
										<div class="account_title">"아래 그룹로 유입된 사람"중</div>
										<div>
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>특정일 동안 미방문 고객</p></div>
													<ul class="select_view">
														<li>이벤트1</li>
														<li>이벤트2</li>
														<li>이벤트3</li>
													</ul>
												</div>
											</div>
										</div>
										<div class="account_date">
											<input type="text"><span>일</span>
										</div>
									</div>
									<div class="account_wrap">
										<div class="account_inner_wrap clearfix">
											<div class="account_left">
												<strong>양식에 맞추어 엑셀을 입력해 주세요.</strong>
												<p>양식에 맞추어 엑셀을 업로드 해주시면,</p>
												<p>해당 파라미터를 타겟으로 만들 수 있습니다.</p>
												<div class="excel_wrap">
													<div class="download_wrap clearfix">
														<button><strong>엑셀업로드</strong></button>
														<button>양식 다운로드</button>
													</div>
													<div class="input_wrap clearfix">
														<div>
															<input type="text">
														</div>
														<button></button>
													</div>
													<button class="upload_btn"><strong>업로드</strong></button>
												</div>
											</div>
											<div class="account_right clearfix">
												<button><img src="images/target/target_close_btn.png" alt=""></button>
												<ul>
													<li>
														<span>모바일 DA_페이스북 (질바이질슈즈)</span> <span><img src="images/target/target_list_close.png" alt=""></span>
													</li>
													<li>
														<span>모바일 DA_페이스북 (질바이질슈즈)</span> <span><img src="images/target/target_list_close.png" alt=""></span>
													</li>
													<li>
														<span>모바일 DA_페이스북 (질바이질슈즈)</span> <span><img src="images/target/target_list_close.png" alt=""></span>
													</li>
												</ul>
											</div>
										</div>
									</div>
								</div> -->
								<!-- 엑셀 업로드-->
								<!-- 타겟만들기 미연동시 -->
								<!-- <div class="account_interlock">
									<strong>페이스북 광고 계정과 네오를 연결해 주세요.</strong>
									<p>설정페이지에서 해당 광고 계쩡과 네오를 연결하면,</p>
									<p>빠르고 쉽게 Neo 기반 타겟팅을 만드실 수 있습니다.</p>
									<button>설정페이지로 이동</button>
								</div> -->
								<!-- //타겟만들기 미연동시 -->
								<!-- 타겟만들기 기본형-->
								<!-- <div class="target_generate">
									<div class="account_info">
										<div class="account_title">"사이트 방문자"중</div>
										<div>
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>특정일 동안 미방문 고객</p></div>
													<ul class="select_view">
														<li>이벤트1</li>
														<li>이벤트2</li>
														<li>이벤트3</li>
													</ul>
												</div>
											</div>
										</div>
									</div>
								</div> -->
								<!-- //타겟만들기 기본형-->
								<!-- <div class="target_generate">
									<div class="account_info">
										<div class="account_title">"아래 그룹로 유입된 사람"중</div>
										<div>
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>특정일 동안 미방문 고객</p></div>
													<ul class="select_view">
														<li>이벤트1</li>
														<li>이벤트2</li>
														<li>이벤트3</li>
													</ul>
												</div>
											</div>
										</div>
										<div class="account_date">
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>선택</p></div>
													<ul class="select_view">
														<li>10%</li>
														<li>20%</li>
														<li>30%</li>
													</ul>
												</div>
											</div>
										</div>
									</div>
									<div class="generate_url_list">
										<div class="url_list clearfix">
											<div class="url_select clearfix">
												<div class="select_btn">
													<div class="select_contents">
														<div class="select"><p>선택</p></div>
														<ul class="select_view">
															<li>10%</li>
															<li>20%</li>
															<li>30%</li>
														</ul>
													</div>
												</div>
											</div>
											<div class="url_input">
												<input type="text">
											</div>
										</div>
										<div class="url_list clearfix">
											<div class="url_select clearfix">
												<div class="select_btn">
													<div class="select_contents">
														<div class="select"><p>선택</p></div>
														<ul class="select_view">
															<li>10%</li>
															<li>20%</li>
															<li>30%</li>
														</ul>
													</div>
												</div>
											</div>
											<div class="url_input">
												<input type="text">
											</div>
										</div>
										<div class="url_list clearfix">
											<div class="url_select clearfix">
												<div class="select_btn">
													<div class="select_contents">
														<div class="select"><p>선택</p></div>
														<ul class="select_view">
															<li>10%</li>
															<li>20%</li>
															<li>30%</li>
														</ul>
													</div>
												</div>
											</div>
											<div class="url_input">
												<input type="text">
											</div>
										</div>
									</div>
								</div> -->
								<!-- 구글 애널리틱스 -->
								<!-- <div class="target_generate google_analytics">
									<div class="account_info">
										<div class="account_title">"아래 UTM 속성으로 유입된 사람" 중</div>
										<div>
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>이용시간 상위 고객</p></div>
													<ul class="select_view">
														<li>이벤트1</li>
														<li>이벤트2</li>
														<li>이벤트3</li>
													</ul>
												</div>
											</div>
										</div>
										<div class="account_date">
											<div class="select_btn">
												<div class="select_contents">
													<div class="select"><p>선택</p></div>
													<ul class="select_view">
														<li>25%</li>
														<li>50%</li>
														<li>75%</li>
													</ul>
												</div>
											</div>
										</div>
									</div>
									<div class="generate_url_list">
										<div class="url_list clearfix">
											<div class="url_select clearfix">
												<div class="select_btn">
													<div class="select_contents">
														<div class="select"><p>utm_source</p></div>
														<ul class="select_view">
															<li>10%</li>
															<li>20%</li>
															<li>30%</li>
														</ul>
													</div>
												</div>
											</div>
											<div class="url_input">
												<input type="text" placeholder="값 입력 후 엔터를 치면 아래에 입력됩니다.">
											</div>
										</div>
									</div>
								</div> -->
								<!-- // 구글 애널리틱스 -->
							</div>
							<!-- 구글 애널리틱스 -->
							<!-- <div class="analytics_tab_wrap">
								<div class="analytics_tab_widget clearfix">
									<ul class="clearfix">
										<li rel="tab_list_1" class="active">source</li>
										<li rel="tab_list_2">medium</li>
										<li rel="tab_list_3">campaign</li>
										<li rel="tab_list_4">team</li>
										<li rel="tab_list_5">content</li>
										<li rel="tab_list_6">custom</li>
									</ul>
								</div>
								<div class="analytics_tab_list">
									<div id="tab_list_1" class="analytics_tab_contents clearfix">
										<ul>
											<li class="sticker_btn"><span>naver</span></li>
											<li class="sticker_btn"><span>daum</span></li>
											<li class="sticker_btn"><span>google</span></li>
										</ul>
									</div>
									<div id="tab_list_2" class="analytics_tab_contents clearfix"></div>
									<div id="tab_list_3" class="analytics_tab_contents clearfix"></div>
									<div id="tab_list_4" class="analytics_tab_contents clearfix"></div>
									<div id="tab_list_5" class="analytics_tab_contents clearfix"></div>
									<div id="tab_list_6" class="analytics_tab_contents clearfix"></div>
								</div>
							</div> -->
							<!-- // 구글 애널리틱스 -->
						</div>
					</div>
					<div class="btn_wrap">
						<button class="before_btn close_pop">취소</button>
						<button class="next_btn">타겟 만들기</button>
					</div>
					<div class="btn_wrap">
						<button class="before_btn close_pop">취소</button>
						<button class="delete_btn">타겟 삭제</button>
						<button class="adjust_btn">타겟 수정</button>
					</div>
				</div>
				<p class="popup-btn"><button type="button" id="close-btn" class="close-btn close_pop">X</button></p>
			</div>
		</div>
	</div>

</template>

<script>
export default {

  name: 'TargetMake02',

  data () {
    return {

    }
  }
}
</script>

<style lang="css" scoped>
</style>