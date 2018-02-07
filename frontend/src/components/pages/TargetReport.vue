<template>
	<div id="main_wrap" class="clearfix">
		<div id="container">
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div id="report-widget" class="tab-contents-widget">
						<div id="section_list_2" class="section_tab_contents clearfix">
							<div class="target_contents_wrap">
								<div class="target_search_wrap clearfix">
									<div class="cate_select">
										<p>카테고리</p>
										<ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select>
									</div>
									<div class="admin_select">
										<p>광고계정</p>
										<ui-select :selectData="this.accountSelectData" :onClick="selectAccount"></ui-select>
									</div>
									<div class="data_select">
										<p>기간</p>
										<div class="select_btn">
											<div class="select_contents">
												<ui-calendar v-model="range"></ui-calendar>
											</div>
										</div>
									</div>
									<button class="report_search" v-on:click="getGridData()">검색</button>
								</div>
								<div class="target_report_wrap" v-show="isReport">
									<div class="target_setup">
										<div class="select_btn">
											<div class="select_contents control-select">
												<div class="select" v-on:click="sortSelectOnOff()"><p>열 맞춤 설정</p></div>
												<ul class="select_view control_view" v-if="this.sortSelectData.onShow">
													<li v-for="item in this.sortSelectData.listData"><input type="checkbox" v-bind:id="item.setting.checkId" v-on:change="sortSelectFilter(item)" :checked="item.setting.checked"><label v-bind:for="item.setting.checkId">{{ item.setting.name }}</label></li>
												</ul>
											</div>
										</div>
										<button>
											<span>
												<img src="../../assets/images/icon/excel_icon.png" alt="">
											</span>
											<span v-on:click="downloadReport()">엑셀로 내보내기</span>
										</button>
									</div>
									<div class="target_report_contents">
										<div class="report_contents_inner_wrap">
											<div id="report-list" class="contents_inner">
												<div class="table_head">
													<ul id="report-list-head" class="head_th clearfix">
														<li class="line-1 report-line" v-if="sortSelectData.listData[0].setting.show">광고주</li>
														<li class="line-2 normal_depth report-line" v-if="sortSelectData.listData[1].setting.show">캠페인명</li>
														<li class="line-3 report-line" v-if="sortSelectData.listData[2].setting.show">기간</li>
														<li class="line-4 normal_depth report-line" v-if="sortSelectData.listData[3].setting.show">광고세트</li>
														<li class="line-5 report-line" v-if="sortSelectData.listData[4].setting.show">연령</li>
														<li class="line-6 report-line" v-if="sortSelectData.listData[5].setting.show">성별</li>
														<li class="line-7 report-line" v-if="sortSelectData.listData[6].setting.show">관심사 개수</li>
														<li class="line-8 normal_depth report-line" v-if="sortSelectData.listData[7].setting.show">맞춤타겟 이름</li>
														<li class="line-9 report-line" v-if="sortSelectData.listData[8].setting.show">
															<span>광고비</span>
															<span class="sort_type_01">
																<div>
																	<p><a href="javascript:void(0)" v-on:click="listSort('spend','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																	<p><a href="javascript:void(0)" v-on:click="listSort('spend','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																</div>
															</span>
														</li>
														<li class="line-10 report-line" v-if="sortSelectData.listData[9].setting.show">
															<span>노출</span>
															<span class="sort_type_01">
																<div>
																	<p><a href="javascript:void(0)" v-on:click="listSort('impressions','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																	<p><a href="javascript:void(0)" v-on:click="listSort('impressions','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																</div>
															</span>
														</li>
														<li class="line-11 report-line" v-if="sortSelectData.listData[10].setting.show">
															<span>도달</span>
															<span class="sort_type_01">
																<div>
																	<p><a href="javascript:void(0)" v-on:click="listSort('reach','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																	<p><a href="javascript:void(0)" v-on:click="listSort('reach','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																</div>
															</span>
														</li>
														<li class="line-12 report-line" v-if="sortSelectData.listData[11].setting.show">
															<span>도달빈도</span>
															<span class="sort_type_01">
																<div>
																	<p><a href="javascript:void(0)" v-on:click="listSort('frequency','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																	<p><a href="javascript:void(0)" v-on:click="listSort('frequency','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																</div>
															</span>
														</li>
														<li class="line-13 th_sub depth1 report-line" v-if="sortSelectData.listData[12].setting.show">
															<dl>
																<dt>사이트 유입 지표</dt>
																<dd>
																	<ul class="clearfix">
																		<li v-if="sortSelectData.listData[12].setting.show">
																			<span>링크클릭</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('inline_link_clicks','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('inline_link_clicks','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[12].setting.show">
																			<span>CTR</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('inline_link_click_ctr','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('inline_link_click_ctr','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[12].setting.show">
																			<span>CPC</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('linkCpc','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('linkCpc','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																	</ul>
																</dd>
															</dl>
														</li>
														<li class="line-14 th_sub depth2 report-line" v-if="sortSelectData.listData[13].setting.show">
															<dl>
																<dt>슬라이드 소재 클릭 지표</dt>
																<dd>
																	<ul class="clearfix">
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>1번</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick1','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick1','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>2번</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick2','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick2','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>3번</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick3','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick3','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>4번</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick4','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick4','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>5번</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick5','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick5','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>6번</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick6','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('sClick6','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																	</ul>
																</dd>
															</dl>
														</li>
														<li class="line-15 th_sub depth3 report-line" v-if="sortSelectData.listData[14].setting.show">
															<dl>
																<dt>영상캠페인 지표</dt>
																<dd>
																	<ul class="clearfix">
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>10초 이상 View</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_10_sec_watched_actions','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_10_sec_watched_actions','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>10초 이상 VTR</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_10_sec_watched_vtr','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_10_sec_watched_vtr','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>10초 이상 CPV</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_10_sec_watched_cpv','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_10_sec_watched_cpv','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>30초 이상 View</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_30_sec_watched_actions','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_30_sec_watched_actions','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>30초 이상 VTR</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_30_sec_watched_vtr','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_30_sec_watched_vtr','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>30초 이상 CPV</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_30_sec_watched_cpv','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('video_30_sec_watched_cpv','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																	</ul>
																</dd>
															</dl>
														</li>
														<li class="line-16 th_sub depth4 report-line" v-if="sortSelectData.listData[15].setting.show">
															<dl>
																<dt>전환 지표</dt>
																<dd>
																	<ul class="clearfix">
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>전환 완료</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>전환 완료 가치</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResultWorth','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResultWorth','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>1단계 완료</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult1','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult1','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>2단계 완료</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult2','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult2','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>3단계 완료</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult3','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult3','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>4단계 완료</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult4','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult4','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>5단계 완료</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult5','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('convResult5','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																	</ul>
																</dd>
															</dl>
														</li>
														<li class="line-17 th_sub depth5 report-line" v-if="sortSelectData.listData[16].setting.show">
															<dl>
																<dt>페이지 참여 지표</dt>
																<dd>
																	<ul class="clearfix">
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>공유</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('post_event','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('post_event','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>좋아요</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('like_event','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('like_event','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>댓글</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('comment_event','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('comment_event','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>공감</span>
																			<span class="sort_type_02">
																				<div>
																					<p><a href="javascript:void(0)" v-on:click="listSort('post_reaction_event','ASC')"><img src="../../assets/images/icon/report_up.png" alt=""></a></p>
																					<p><a href="javascript:void(0)" v-on:click="listSort('post_reaction_event','DESC')"><img src="../../assets/images/icon/report_down.png" alt=""></a></p>
																				</div>
																			</span>
																		</li>
																	</ul>
																</dd>
															</dl>
														</li>
													</ul>
												</div>
												<div class="table_body">
													<div class="table_body_inner" v-for="(item, index) in listData.data">
														<ul class="body_th clearfix">
															<input id="hidden-interest" type="text" :value="item.interest_list" ref="interest_copy">
															<li class="line-1" v-if="sortSelectData.listData[0].setting.show">{{ item.account_name }}</li>
															<li class="line-2 normal_depth" v-if="sortSelectData.listData[1].setting.show">{{ item.campaign_name }}</li>
															<li class="line-3" v-if="sortSelectData.listData[2].setting.show">{{ item.report_date }}</li>
															<li class="line-4 normal_depth" v-if="sortSelectData.listData[3].setting.show">{{ item.adset_name }}</li>
															<li class="line-5" v-if="sortSelectData.listData[4].setting.show">{{ item.age }} 세</li>
															<li class="line-6" v-if="sortSelectData.listData[5].setting.show">{{ item.gender }}</li>
															<li class="interest line-7" v-if="sortSelectData.listData[6].setting.show">
																<span :class="'interest-sub-' + index" @click="tootip(index)">{{ item.interest_num }} 개</span>
																<div :id="'interest-sub-' + index" class="interest_view" v-if="item.interest_list.length != 0">
																	<ul class="clearfix">
																		<li v-for="elem in item.interest_list" >{{ elem }}</li>
																	</ul>
																	<div class="inter_clip_copy" v-on:click="clickCopy(index)">클립보드로 복사하기</div>
																	<div class="inter_close" @click="tootip('close')">닫기</div>
																</div>
															</li>
															<li class="line-8 normal_depth" v-if="sortSelectData.listData[7].setting.show"><span v-for="ca in item.custom_audience">{{ ca }}</span></li>
															<li class="line-9 box-align" v-if="sortSelectData.listData[8].setting.show">￦{{ numberFormat(item.spend) }}</li>
															<li class="line-10 box-align" v-if="sortSelectData.listData[9].setting.show">{{ numberFormat(item.impressions) }}</li>
															<li class="line-11 box-align" v-if="sortSelectData.listData[10].setting.show">{{ numberFormat(item.reach) }}</li>
															<li class="line-12 box-align" v-if="sortSelectData.listData[11].setting.show">{{ numberFormat(item.frequency) }}</li>
															<li class="line-13 depth1" v-if="sortSelectData.listData[12].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li>{{ numberFormat(item.inline_link_clicks) }}</li>
																			<li>{{ item.inline_link_click_ctr }}</li>
																			<li>￦{{ numberFormat((item.spend / item.inline_link_clicks).toFixed(0)) }}</li>
																		</ul>
																	</dd>
																</dl>
															</li>
															<li class="line-14 depth2" v-if="sortSelectData.listData[13].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li>-</li>
																			<li>-</li>
																			<li>-</li>
																			<li>-</li>
																			<li>-</li>
																			<li>-</li>
																		</ul>
																	</dd>
																</dl>
															</li>
															<li class="line-15 depth3" v-if="sortSelectData.listData[14].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li class="line-15">{{ item.video_10_sec_watched_actions }}</li>
																			<li class="line-15">{{ item.video_10_sec_watched_vtr }}</li>
																			<li class="line-15">￦{{ item.video_10_sec_watched_cpv }}</li>
																			<li class="line-15">{{ item.video_30_sec_watched_actions }}</li>
																			<li class="line-15">{{ item.video_30_sec_watched_vtr }}</li>
																			<li class="line-15">￦{{ item.video_30_sec_watched_cpv }}</li>
																		</ul>
																	</dd>
																</dl>
															</li>

															<li class="line-16 depth4" v-if="sortSelectData.listData[15].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li class="line-16">{{ getCustomMappingEvent(item, '전환완료') }}</li>
																			<!-- cost_per_action_type?-->
																			<li class="line-16">{{ (convTotal / item.spend).toFixed(2) }}</li>
																			<li class="line-16">{{ getCustomMappingEvent(item, '전환 1단계') }}</li>
																			<li class="line-16">{{ getCustomMappingEvent(item, '전환 2단계') }}</li>
																			<li class="line-16">{{ getCustomMappingEvent(item, '전환 3단계') }}</li>
																			<li class="line-16">{{ getCustomMappingEvent(item, '전환 4단계') }}</li>
																			<li class="line-16">{{ getCustomMappingEvent(item, '전환 5단계') }}</li>
																		</ul>
																	</dd>
																</dl>
															</li>
															<li class="line-17 depth5" v-if="sortSelectData.listData[16].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li class="line-17">{{ item.post_event }}</li>
																			<li class="line-17">{{ item.like_event }}</li>
																			<li class="line-17">{{ item.comment_event }}</li>
																			<li class="line-17">{{ item.post_reaction_event }}</li>
																		</ul>
																	</dd>
																</dl>
															</li>
														</ul>
													</div>
												</div>
											</div>
										</div>
									</div>
									<!-- TODO Paging 처리 예정 -->
									<div class="pagination">
										<ul>
											<li v-show="currentPage > 1" v-on:click="clickFirstPage(firstPage)"><img src="../../assets/images/icon/paging_01.png" alt="" v-if="!loadShow"><img src="../../assets/images/icon/loading.gif" alt="로딩중" class="loading-img" v-if="loadShow" style="width:100%"></li>
											<li v-show="currentPage > 1" v-on:click="clickPreviousPage(currentPage)"><img src="../../assets/images/icon/paging_03.png" alt="" v-if="!loadShow"><img src="../../assets/images/icon/loading.gif" alt="로딩중" class="loading-img" v-if="loadShow" style="width:100%"></li>
											<!-- <li class="now">1</li> -->
											<li v-for="(n,index) in pageRange.pageNumber" v-if="(n >= pageRange.minPaging)&&(n <= pageRange.maxPaging)" v-on:click="clickPage(n)"
												v-bind:class="[currentPage === n ? 'now' : '']"><span v-if="!loadShow">{{ checkPageNumber(n) }}</span><img src="../../assets/images/icon/loading.gif" alt="로딩중" class="loading-img" v-if="loadShow" style="width:100%"></li>
											<li v-show="currentPage < pageRange.pageNumber" v-on:click="clickNextPage(currentPage)"><img src="../../assets/images/icon/paging_04.png" alt="" v-if="!loadShow"><img src="../../assets/images/icon/loading.gif" alt="로딩중" class="loading-img" v-if="loadShow" style="width:100%"></li>
											<li v-show="currentPage < pageRange.pageNumber" v-on:click="clickLastPage(pageRange.pageNumber)"><img src="../../assets/images/icon/paging_02.png" alt="" v-if="!loadShow"><img src="../../assets/images/icon/loading.gif" alt="로딩중" class="loading-img" v-if="loadShow" style="width:100%"></li>
										</ul>
									</div>
								</div>
							</div>

							<ui-loading :isShow="isLoading" :titleText="loadingTitle" :descriptionText="loadingDescription"></ui-loading>
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
import Calendar from '@/components/ui/Calendar'
import Loading from '@/components/ui/Loading'
import PartialLoading from '@/components/ui/PartialLoading'
import { numberToFixed, numberFormatter } from '@/components/utils/Formatter'

export default {
	name: 'TargetReport',

	components: {
		'ui-select': Select,
		'ui-calendar': Calendar,
		'ui-loading': Loading,
		'ui-partial-loading': PartialLoading
	},

	beforeMount () {
		this.setDatas()
	},

	mounted () {
		this.sortTableAutoWidth()
		this.wResize()
		window.addEventListener('resize', this.wResize)
		this.getGridData()
	},

	beforeDestroy () {
		window.removeEventListener('resize', this.wResize)
	},
	created () {
		this.loadFbAdAccounts()
	},

	// mounted () {
	// 	this.loadFbAdAccounts()
	// },

	data () {
		return {
			loadShow:false,
			pageRange: {
				//페이지 번호
				pageNumber:1,
				//최소 페이징
				minPaging:0,
				//최대 페이징
				maxPaging:10,
				//노출 페이징 갯수
				showPaging:10
			},
			categorySelectData: {
				emptyText: '전체',
				textList: [
					'전체',
					'대출',
					'카드',
					'보험',
					'뷰티',
					'NGO',
					'여행',
					'쇼핑몰',
					'기타'
				],
				keyList: [
					'all',
					'loan',
					'card',
					'insurance',
					'beauty',
					'ngo',
					'travel',
					'shoppingmall',
					'etc'
				]
			},
			accountSelectData: {
				emptyText: '전체',
				textList: [
				],
				keyList: [
				]
			},
			sortSelectData: {
				emptyText: '열 맞춤 설정',
				onShow:false,
				listData: [],
			},

			listData:{
				data: []
			},

			pageTotal: 0,
			currentPage: 1,
			firstPage: 1,
			convTotal: 0,

			tablesAutoWidth:4880,


			show: false,
			time: new Date(),
			range: [new Date("October 13, 2010 11:13:00"),new Date()],
			emptyTime: '',
			emptyRange: [],
			local: {
				type: Object,
				default () {
					return {
						dow: 0, // Sunday is the first day of the week
						hourTip: 'Select Hour', // tip of select hour
						minuteTip: 'Select Minute', // tip of select minute
						secondTip: 'Select Second', // tip of select second
						yearSuffix: '', // suffix of head year
						yearSuffix: '년', // format of head
						monthsHead: '1월_2월_3월_4월_5월_6월_7월_8월_9월_10월_11월_12월'.split('_'), // months of head
						months: '1월_2월_3월_4월_5월_6월_7월_8월_9월_10월_11월_12월'.split('_'), // months of panel
						weeks: '일_월_화_수_목_금_토'.split('_') // weeks
					}
				}
			},

			isReport: true,
			isLoading: false,
			loadingTitle: '',
			loadingDescription: ''
		}
	},

	methods: {
		wResize (){
			const wSize = window.innerWidth - 185
			const el = document.getElementById('report-widget')
			el.style = "width:" + wSize + 'px'
		},

		tootip (index) {
			const tools = document.getElementsByClassName('interest_view')
			const subId = event.target.className
			const subEl = document.getElementById(subId)
			for(let i = 0; i < tools.length; i++) {
				tools[i].style = "display:none"
			}
			if (subEl !== null) {
				if(index != 'close') {
					if(subEl.style.display == 'block') {
						subEl.style = "display:none"
					}else{
						subEl.style = "display:block"
					}
				}
			}
		},

		setDatas () {

			const label = ['광고주','캠페인명','기간','광고세트','연령','성별','관심사 개수','맞춤타겟 이름','광고비','노출','도달','도달빈도','사이트 유입 지표','슬라이드 소재 클릭 지표','영상캠페인 지표','전환 지표','페이지 참여 지표']
			const sortData = []

			for(let i = 0; i < label.length; i++) {
				let setting = {
					setting:{
						name:label[i],
						checkId:'sort' + i,
						show:true,
						checked:true
					}
				}
				this.sortSelectData.listData.push(setting)
			}
		},

		selectCategory (item) {
			this.categorySelectData.emptyText = item
			this.loadFbAdAccounts()
		},

		selectAccount (item) {
			this.accountSelectData.emptyText = item
		},

		sortSelectOnOff () {
			this.sortSelectData.onShow = !this.sortSelectData.onShow
		},

		sortSelectFilter (item) {
			const me = this
			item.setting.checked = !item.setting.checked
			item.setting.show = !item.setting.show
			setTimeout(function() {
				me.sortTableAutoWidth()
			}, 1)
		},

		sortTableAutoWidth (){
			const listEl = document.getElementById('report-list')
			const ulEl = document.getElementById('report-list-head')
			const liEl = ulEl.getElementsByClassName('report-line')
			let listWidth = 0

			for(let i = 0; i < liEl.length; i++) {
				listWidth += liEl[i].offsetWidth
			}

			this.tablesAutoWidth = listWidth
			listEl.style.width = this.tablesAutoWidth + 'px'
		},

		listSort(key, type) {
			const item = this.listData.data
			//숫자 형식 소팅(String,Text 형식 지원 X)
			const byNum = item.slice(0)
			byNum.sort(function(a,b) {
				if(type == 'ASC') {
						return a[key] - b[key]
				}else{
						return b[key] - a[key]
				}
			})
			this.listData.data = byNum
			//Event Arrow On Off

		},

		disabledDate (time) {
			return time < this.min || time > this.max
		},
		dc (e) {
			this.show = this.$el.contains(e.target) && !this.disabled
		},

		loadFbAdAccounts () {
			// fb_ad_accounts/accounts_by_category
			// DB 저장 된 광고 계정 리스트 가져오기
			let url = '/fb_ad_accounts/accounts_by_category'
			this.$http.get(url, {
				params: {
					account_category: this.findSelectKey('categorySelectData')
				}
			})
			.then(res => {
				const response = res.data
				const data = response.data
				const success = response.success

				if (success === "YES") {
					if (data.length > 0) {
						var accountNameList = []
						var acountIdList = []
						data.forEach(item => {
							accountNameList.push(item.name)
							acountIdList.push(item.ad_account_id)
						})
						this.accountSelectData.textList = accountNameList
						this.accountSelectData.keyList = acountIdList
						this.accountSelectData.textList.splice(0, 0, "전체")
						this.accountSelectData.keyList.splice(0, 0, 0)
						this.accountSelectData.emptyText = accountNameList[0]
					} else {
						this.accountSelectData.emptyText = '광고주 없음'
						this.accountSelectData.textList = []
						this.accountSelectData.keyList = []
					}
				}
			})
			.catch(err => {
				console.error('/fb_ad_accounts/accounts_by_category', err)
			})
		},

		findSelectKey (selectName) {
			/*
			Select Key 가져오기
			*/
			const emptyText = this[selectName].emptyText
			const textList = this[selectName].textList
			const keyList = this[selectName].keyList
			return keyList[textList.indexOf(emptyText)]
		},

		getPageNumber () {
			var limit = 25
			var page_total = this.pageTotal
			var page_number = page_total / limit
			this.pageRange.pageNumber = Math.round(page_number)
		},
		clickPage (n) {
			this.currentPage = n
			this.getGridData('paging')
		},
		clickFirstPage (n) {
			this.currentPage = n
			this.pageRange.minPaging = 1
			this.pageRange.maxPaging = 10
			this.getGridData('paging')
		},
		clickLastPage(n) {
			const nString = String(n)
			const nlength = nString.length
			const nLast = nString.substring(nlength - 1)
			const nCal = n - Number(nLast)

			this.currentPage = n
			this.pageRange.minPaging = nCal + 1
			this.pageRange.maxPaging = n

			this.getGridData('paging')
		},

		checkPageNumber (n) {
			return n
		},

		clickNextPage (p) {
			this.currentPage = p + 1
			// const pageRange = Array.from({length: this.pageNumber}, (v, k) => k+1)
			if(this.pageRange.maxPaging < this.currentPage) {
				this.pageRange.minPaging = this.currentPage
				this.pageRange.maxPaging = this.pageRange.minPaging + this.pageRange.showPaging - 1
				if(this.pageRange.maxPaging > this.pageRange.pageNumber) {
					this.pageRange.maxPaging = this.pageRange.pageNumber
				}
			}
			this.getGridData('paging')
		},

		clickPreviousPage (p) {
			this.currentPage = p - 1
			if(this.pageRange.minPaging > this.currentPage) {
				if(this.currentPage < this.pageRange.showPaging + 1) {
					this.pageRange.minPaging = this.pageRange.minPaging - this.pageRange.showPaging - 1
					this.pageRange.maxPaging = this.pageRange.minPaging + this.pageRange.showPaging
				}else{
					this.pageRange.minPaging = this.pageRange.minPaging - this.pageRange.showPaging
					this.pageRange.maxPaging = this.pageRange.minPaging + this.pageRange.showPaging - 1
				}
			}
			this.getGridData('paging')
		},

		getGridData (type) {
			var date_range = []
			this.range.forEach(date => {
				date_range.push(date.toISOString().split('T')[0])
			})

			this.listData.data = []
			if(type == 'paging') {
				//부분 로딩 추가 예정
				this.loadShow = true
			} else{
				this.isReport = false
				this.loadShow = false
				this.isLoading = true
				this.loadingTitle = '인사이트를 가져오는 중입니다.'
				this.loadingDescription = '조금만 기다려 주시면, 인사이트를 가져옵니다.'
			}

			let url = '/ad_set_insights'
			this.$http.get(url, {
				params: {
					account_id: this.findSelectKey('accountSelectData'),
					category_name: this.findSelectKey('categorySelectData'),
					since: date_range[0],
					until: date_range[1],
					page: this.currentPage
				}
			})
			.then(res => {
				const response = res.data
				const data = response.data
				const total = response.total_count
				const success = response.success
				if (success === "YES") {
					data.forEach(item => {
						this.listData.data.push(item)
					})
					this.pageTotal = total
					this.isReport = true
					this.isLoading = false
					this.loadShow = false
					this.getPageNumber()
				} else {
					throw('success: ' + success)
					this.isReport = true
					this.isLoading = false
					this.loadShow = false
				}
			})
			.catch(err => {
				this.isLoading = false
				this.loadShow = false
				console.error('/ad_set_insights', err)
			})
		},

		getCustomMappingEvent (item, type) {
			const pixel_event = item.pickdata_custom_pixel_event
			let value = 0
			pixel_event.forEach(elem => {
				const name = elem.custom_name
				if (name == type) {
					value = elem.value
					if (type == '전환완료') {
						this.convTotal = elem.value
					} else {
						pass
					}
				}
				else {
					// return 0
				}
			})
			return value
		},

		downloadReport () {
			console.log('download')
			var date_range = []
			this.range.forEach(date => {
				date_range.push(date.toISOString().split('T')[0])
			})
			const account_id = this.findSelectKey('accountSelectData')
			const category_name = this.findSelectKey('categorySelectData')
			const since = date_range[0]
			const until = date_range[1]

			// ad_set_insights/?account_id=349408409&since=2018-01-01&until=2018-01-15
			let url = '/ad_set_insights/download?account_id=' + account_id + '&category_name=' + category_name + '&since=' + since + '&until=' + until
			window.open(url, '_blank')
		},

		numberFormat (n) {
			if (typeof n === typeof undefined || n == null) {
				return 0
			}
			return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
		},

		checkObject (n) {
			if (typeof n === typeof undefined || n == null) {
				return 0
			}
		},

		clickCopy (index) {
			var result
			this.$refs.interest_copy[index].select();
			result = document.execCommand('copy')
			return result
		}
	}
}
</script>

<style lang="css" scoped>
#hidden-interest { float:left; height:0; }
</style>
