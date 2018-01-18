<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="target_pop_01">
						<div class="popup-contents clearfix">
							<div class="pop_title_wrap">
								<div class="pop_title">타겟 만들기 (<span id="page-number">1</span>/2)</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close_pop close-btn" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>

							<!-- 카테고리 선택 탭 -->
							<div class="pop_tab_wrap clearfix" v-if="tabAction.tabActive1.show">
								<div class="cate_contents_widget">
									<ul class="target_pick_01">
										<li @click="tabMove(1)">
											<span>사이트방문</span>
										</li>
										<li @click="tabMove(2)">
											<span>특정페이지 방문</span>
										</li>
										<li @click="tabMove(3)">
											<span>NEO 타겟</span>
										</li>
										<li @click="tabMove(4)">
											<span>구글애널리틱스</span>
										</li>
									</ul>
									<ul class="target_pick_02">
										<li @click="tabMove(5)">
											<span>구매</span>
										</li>
										<li @click="tabMove(6)">
											<span>장바구니</span>
										</li>
										<li @click="tabMove(7)">
											<span>회원가입</span>
										</li>
										<li @click="tabMove(8)">
											<span>단계별 전환</span>
										</li>
									</ul>
								</div>
								<div class="btn_wrap">
									<button type="button" class="close_pop" @click="$emit('close')">취소</button>
								</div>
							</div>


							<!-- 사이트 방문 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive2.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="target_generate">
												<div class="account_info">
													<div class="account_title">"사이트 방문자"중</div>
													<div>
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
							</div>

							<!-- 특정 페이지 방문 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive3.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_02.png" alt="neo"></div>
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="target_generate">
												<div class="account_info">
													<div class="account_title">"아래 그룹로 유입된 사람"중</div>
													<div>
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
													<div class="account_date">
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
												</div>
												<div class="generate_url_list">

													<div v-for="(item, index) in fields" class="url_list clearfix">
														<div class="url_select clearfix" :data-key="item.key">
															<ui-select :selectData="item.select" @click="multiSelect(item, index)"></ui-select>
														</div>
														<div class="url_input">
															<input type="text">
														</div>
														<div class="url_btn clearfix">
															<div class="add"><button type="button" @click="fieldBtn(item,'add')">+</button></div>
															<div class="del"><button type="button" @click="fieldBtn(item,'del')">-</button></div>
														</div>
													</div>

												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
							</div>

							<!-- 네오 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive4.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_03.png" alt="neo"></div>
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
													<div class="result_check"><input type="radio" id="target_type01" @change="neoTab('media')" name="neo_type" value="media" checked><label for="target_type01">매체</label></div>
												</li>
												<li>
													<div class="result_check"><input type="radio" id="target_type02" name="neo_type" @change="neoTab('group')" value="group"><label for="target_type02">그룹</label></div>
												</li>
												<li>
													<div class="result_check"><input type="radio" id="target_type03" name="neo_type"  @change="neoTab('keyword')" value="keyword"><label for="target_type03">키워드</label></div>
												</li>
												<li>
													<div class="result_check"><input type="radio" id="target_type04" name="neo_type" @change="neoTab('excel')" value="excel"><label for="target_type04">엑셀업로드</label></div>
												</li>
											</ul>
										</div>
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<!-- 매체 -->
											<div class="cate_contents" v-if="tabAction.tabActive4.subActive.media">
												<div class="account_info">
													<div class="account_title">"아래 매체로 유입된 사람"중</div>
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
																				<div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
																				<div class="result_account">계정명</div>
																				<div class="result_group">캠페인명</div>
																				<div class="result_switch">전환 수</div>
																			</li>
																		</ul>
																	</div>
																	<div class="result_tbody">
																		<ul id="adv-list-1">
																			<li v-for="adv in advs">
																				<div class="result_check"><input type="checkbox" v-model="selected" :value="adv.number" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.number"><label :for="'adv-check-' + adv.number"></label></div>
																				<div class="result_account">{{ adv.name }}</div>
																				<div class="result_group">{{ adv.campaign }}</div>
																				<div class="result_switch">{{ adv.count }}</div>
																			</li>
																		</ul>
																	</div>
																</div>
															</div>
															<div class="account_add_wrap">
																<div>*최근 한달 기준</div>
																<button type="button" v-on:click="checkList('advs','addAdvs')">선택한 매체 추가</button>
															</div>
														</div>
														<div class="account_right clearfix">
															<button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
															<ul id="adv-list-2">
																<li v-for="addAdv in addAdvs" class="sticker_btn">
																	<span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
																</li>
															</ul>
														</div>
													</div>
												</div>
											</div>
											<!-- 그룹 -->
											<div class="cate_contents" v-if="tabAction.tabActive4.subActive.group">
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
																				<div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
																				<div class="result_account">계정명</div>
																				<div class="result_group">그룹명</div>
																				<div class="result_switch">전환 수</div>
																			</li>
																		</ul>
																	</div>
																	<div class="result_tbody">
																		<ul id="adv-list-1">
																			<li v-for="adv in advs">
																				<div class="result_check"><input type="checkbox" v-model="selected" :value="adv.number" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.number"><label :for="'adv-check-' + adv.number"></label></div>
																				<div class="result_account">{{ adv.name }}</div>
																				<div class="result_group">{{ adv.campaign }}</div>
																				<div class="result_switch">{{ adv.count }}</div>
																			</li>
																		</ul>
																	</div>
																</div>
															</div>
															<div class="account_add_wrap">
																<div>*최근 한달 기준</div>
																<button type="button" v-on:click="checkList('advs','addAdvs')">선택한 매체 추가</button>
															</div>
														</div>
														<div class="account_right clearfix">
															<button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
															<ul id="adv-list-2">
																<li v-for="addAdv in addAdvs" class="sticker_btn">
																	<span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
																</li>
															</ul>
														</div>
													</div>
												</div>
											</div>
											<!-- 키워드 -->
											<div class="cate_contents" v-if="tabAction.tabActive4.subActive.keyword">
												<div class="account_info">
													<div class="account_title">"아래 키워드로 유입된 사람"중</div>
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
																				<div class="result_check"><input type="checkbox" id="all_check" v-model="selectAll"><label for="all_check"></label></div>
																				<div class="result_account">그룹명</div>
																				<div class="result_group">키워드</div>
																				<div class="result_switch">전환 수</div>
																			</li>
																		</ul>
																	</div>
																	<div class="result_tbody">
																		<ul id="adv-list-1">
																			<li v-for="adv in advs">
																				<div class="result_check"><input type="checkbox" v-model="selected" :value="adv.number" class="result-checkbox" :data-type="'advs'" :data-id="adv.type_id" :id="'adv-check-' + adv.number"><label :for="'adv-check-' + adv.number"></label></div>
																				<div class="result_account">{{ adv.name }}</div>
																				<div class="result_group">{{ adv.campaign }}</div>
																				<div class="result_switch">{{ adv.count }}</div>
																			</li>
																		</ul>
																	</div>
																</div>
															</div>
															<div class="account_add_wrap">
																<div>*최근 한달 기준</div>
																<button type="button" v-on:click="checkList('advs','addAdvs')">선택한 매체 추가</button>
															</div>
														</div>
														<div class="account_right clearfix">
															<button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
															<ul id="adv-list-2">
																<li v-for="addAdv in addAdvs" class="sticker_btn">
																	<span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
																</li>
															</ul>
														</div>
													</div>
												</div>
											</div>
											<!-- 엑셀 -->
											<div class="cate_contents target_excel" v-if="tabAction.tabActive4.subActive.excel">
												<div class="account_info">
													<div class="account_title">"아래 등록 양식으로 유입된 사람"중</div>
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
																<button class="upload_btn view_alert"><strong>업로드</strong></button>
															</div>
														</div>
														<div class="account_right clearfix">
															<button type="button" v-on:click="deleteAddAdvs('all')" title="전체삭제"><img src="../../assets/images/target/target_close_btn.png" alt=""></button>
															<ul id="adv-list-2">
																<li v-for="addAdv in addAdvs" class="sticker_btn">
																	<span>{{ addAdv.name }}</span> <span @click="deleteAddAdvs(addAdv)" :data-number="addAdv.number" title="삭제하기"><img src="../../assets/images/target/target_list_close.png" alt=""></span>
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
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="$emit('close')">취소</button>
									<button class="delete_btn">타겟 삭제</button>
									<button class="adjust_btn">타겟 수정</button>
								</div>
							</div>

							<!-- 구글애널리틱스 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive5.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_04.png" alt="neo"></div>
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody google_body clearfix">
											<div class="target_generate google_analytics">
												<div class="account_info">
													<div class="account_title">"아래 UTM 속성으로 유입된 사람" 중</div>
													<div>
														<div class="select_btn">
															<div class="select_contents">
																<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
															</div>
														</div>
													</div>
													<div class="account_date">
														<div class="select_btn">
															<div class="select_contents">
																<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
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
																	<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
																</div>
															</div>
														</div>
														<div class="url_input">
															<input type="text" placeholder="값 입력 후 엔터를 치면 아래에 입력됩니다.">
														</div>
													</div>
												</div>
											</div>
										</div>
										<div class="analytics_tab_wrap">
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
												<div class="list_close_btn"><img src="../../assets/images/target/target_close_btn.png" alt=""></div>
												<div id="tab_list_1" class="analytics_tab_contents clearfix">
													<ul>
														<li class="sticker_btn"><span>naver</span><span><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
														<li class="sticker_btn"><span>daum</span><span><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
														<li class="sticker_btn"><span>google</span><span><img src="../../assets/images/target/target_list_close.png" alt=""></span></li>
													</ul>
													<div class="analytics_all_close"><img src="images/target/target_close_btn.png" alt=""></div>
												</div>
												<div id="tab_list_2" class="analytics_tab_contents clearfix"></div>
												<div id="tab_list_3" class="analytics_tab_contents clearfix"></div>
												<div id="tab_list_4" class="analytics_tab_contents clearfix"></div>
												<div id="tab_list_5" class="analytics_tab_contents clearfix"></div>
												<div id="tab_list_6" class="analytics_tab_contents clearfix"></div>
											</div>
										</div>
										<div class="btn_wrap">
											<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
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

							<!-- 구매 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive6.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
											<div class="title_info">
												<p>구매</p>
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="target_generate">
												<div class="account_info">
													<div class="account_title">"사이트 방문자"중</div>
													<div>
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
							</div>

							<!-- 장바구니 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive7.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
											<div class="title_info">
												<p>장바구니</p>
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="target_generate">
												<div class="account_info">
													<div class="account_title">"사이트 방문자"중</div>
													<div>
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
							</div>

							<!-- 회원가입 탭 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive8.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_01.png" alt="neo"></div>
											<div class="title_info">
												<p>회원가입</p>
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="target_generate">
												<div class="account_info">
													<div class="account_title">"사이트 방문자"중</div>
													<div>
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="btn_wrap">
									<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
									<button class="next_btn">타겟 만들기</button>
								</div>
							</div>

							<!-- 단계별 전환 -->
							<div class="target_contents_wrap pop-scroll clearfix" v-if="tabAction.tabActive9.show">
								<div class="target_contents_inner">
									<div class="target_thead">
										<div class="main_title">
											<div><img src="../../assets/images/target/target_logo_08.png" alt="neo"></div>
											<div class="title_info">
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
									</div>
									<div class="target_tbody">
										<div class="target_inner_tbody clearfix">
											<div class="target_generate">
												<div class="account_info">
													<div>
														<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
													</div>
													<div class="breakaway_wrap">
														<input type="text">
														<p>단계 완료 후 이탈 고객</p>
													</div>
												</div>
												<div class="generate_url_list">
													<div class="url_list clearfix">
														<div class="url_text clearfix">
															<p>해당 단계 완료 URL</p>
														</div>
														<div class="url_input">
															<input type="text">
														</div>
													</div>
													<div class="url_list clearfix">
														<div class="url_text clearfix">
															<p>다음 단계 완료 URL</p>
														</div>
														<div class="url_input">
															<input type="text">
														</div>
													</div>
												</div>
											</div>
										</div>
										<div class="btn_wrap">
											<button class="before_btn close_pop" @click="tabMove(0)">취소</button>
											<button class="next_btn">타겟 만들기</button>
										</div>
									</div>
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
    	tabAction:{
	    	tabActive1:{
	    		show:true
	    	},
	    	tabActive2:{
	    		show:false
	    	},
	    	tabActive3:{
	    		show:false
	    	},
	    	tabActive4:{
	    		show:false,
	    		subActive:{
	    			media:true,
	    			group:false,
	    			keyword:false,
	    			excel:false
	    		}
	    	},
	    	tabActive5:{
	    		show:false
	    	},
	    	tabActive6:{
	    		show:false
	    	},
	    	tabActive7:{
	    		show:false
	    	},
	    	tabActive8:{
	    		show:false
	    	},
	    	tabActive9:{
	    		show:false
	    	}
    	},

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
        },


        advs:[
        	{ "number": "1", "name": "LF몰", "campaign":"페이스북1", "count":"3,716", "type_id":"13" },
		    { "number": "2", "name": "LF몰2", "campaign":"페이스북2", "count":"3,716", "type_id":"11" },
		    { "number": "3", "name": "LF몰3", "campaign":"페이스북3", "count":"3,716", "type_id":"15" },
		    { "number": "4", "name": "LF몰4", "campaign":"페이스북4", "count":"3,716", "type_id":"17" }
        ],
        addAdvs:[],
        checkData:[],
        selected:[],

        fields:[
        	//sample
        	{
        		"number":0,
        		"key":0,
        		"select":{
		          emptyText: 'URL선택',
		          textList: [
		            '전체URL',
		            '부분URL'
		          ]
		        }
        	}
        ],


    }
  },
  methods: {
  	//페이지 방문 추가 삭제
  	fieldBtn(item,type) {
  		let index = 0
  		if(type === 'add') {
  			index++
  			let obj = {
  				"number":index,
        		"key":index,
        		"select":{
		          emptyText: 'URL선택',
		          textList: [
		            '전체URL',
		            '부분URL'
		          ]
		        }
  			}
	  		this.fields.push(obj)
  		}else{
  			index--
  			this.fields.splice(this.fields.indexOf(item), 1)
  		}
  	},
  	//타겟만들기 카테고리 탭
	tabMove(activeNumber, beforeNumber) {
		let tabArray = ['tabActive1','tabActive2','tabActive3','tabActive4','tabActive5','tabActive6','tabActive7','tabActive8','tabActive9']
		let pageNum = (activeNumber == 0) ? '1':'2'

		document.getElementById('page-number').innerText = pageNum

		for(let i = 0; i < tabArray.length; i++) {
			if(i == activeNumber) {
				this.tabAction[tabArray[i]].show = true
			}else{
				this.tabAction[tabArray[i]].show = false
			}
		}
	},
	//네오 카테고리 유형 탭
	neoTab(type) {
		const types = ['media','group','keyword','excel']
		for(let i = 0; i < types.length; i++) {
			if(types[i] == type) {
				this.tabAction['tabActive4'].subActive[type] = true
			}else{
				this.tabAction['tabActive4'].subActive[types[i]] = false
			}
		}
	},
	selectTarget(item) {
		this.selectData.emptyText = item
	},
	multiSelect(item, index) {
		// var wTile = event.target.parentElement.parentElement.parentElement.parentElement.getAttribute('data-key')

		// {
  //       		"number":"1",
  //       		"key":"1",
  //       		"select":{
		//           emptyText: 'URL선택',
		//           textList: [
		//             '전체URL',
		//             '부분URL'
		//           ]
		//         }
  //       	}
		// this.selectData.emptyText = item
		console.log(item)
		console.log(index)
		console.log(event)
		// this.fields[wTile].select.emptyText = item
	},

	//매체 삭제
	deleteAddAdvs(item) {
		let checkAdd = this.addAdvs
		let addListEl = document.getElementById('adv-list-2')
		let addlistLi = addListEl.getElementsByTagName('li')
		if(item === 'all') {
				for(let i = 0; i < addlistLi.length; i++) {
					this.advs.push(checkAdd[i])
				}
				this.addAdvs.splice(0, addlistLi.length)
		}else{
			this.addAdvs.splice(this.addAdvs.indexOf(item), 1)
			this.advs.push(item)
		}
	},

	//전체선택
	allCheck(value,key1,key2,before,after) {
		const me = this
		var selected = []
        if (value) {
            this.checkFilter(key1)
            me[key1].forEach(function (item) {
                selected.push(item.number)
            });
        }
        me[key2] = selected;
	},
	//체크리스트 추가
	checkList (before,after) {

		const me = this

		this.checkFilter(before)

		me[after] = me[after].concat(me.checkData)
		me.checkData.forEach(function(value, index) {
			me[before] = me[before].filter(function(item) {
				return item !== value
			})
		})

		this.selected = []
		me.checkData = []
	},

	//체크 중복 필터
	checkFilter(type) {
		let elId = "adv-list-1"
		let ul = document.getElementById(elId)
		let items = ul.getElementsByTagName("li")
		let itemsData = this[type]

		for (let i = 0; i < items.length; i++) {
			let checkBox = items[i].getElementsByTagName('input')[0].checked
			if(checkBox == true) {
				let checkItemsId = items[i].getElementsByTagName('input')[0].getAttribute('data-id')
				for(let idx = 0; idx < itemsData.length; idx++) {
					if(checkItemsId == itemsData[idx]['type_id']) {
						this.checkData.push(itemsData[idx])
					}
				}
			}
		}
	}
  },
  computed:{
  	selectAll: {
        get: function () {
            let advKeys = Object.keys(this.advs)
        	if(advKeys.length != 0) {
            	return this.advs ? this.selected.length == advKeys.length : false;
            }
        },
        set: function (value) {
            this.allCheck(value,'advs','selected','advs','addAdvs')
        }
    }
  }

}
</script>

<style lang="css" scoped>
</style>
