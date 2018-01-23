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
									<button class="report_search">검색</button>
								</div>
								<div class="target_report_wrap">
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
											<span>엑셀로 내보내기</span>
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
															<span class="sort_btn"></span>
														</li>
														<li class="line-10 report-line" v-if="sortSelectData.listData[9].setting.show">
															<span>노출</span>
															<span class="sort_btn"></span>
														</li>
														<li class="line-11 report-line" v-if="sortSelectData.listData[10].setting.show">
															<span>도달</span>
															<span class="sort_btn"></span>
														</li>
														<li class="line-12 report-line" v-if="sortSelectData.listData[11].setting.show">
															<span>도달빈도</span>
															<span class="sort_btn"></span>
														</li>
														<li class="line-13 th_sub depth1 report-line" v-if="sortSelectData.listData[12].setting.show">
															<dl>
																<dt>사이트 유입 지표</dt>
																<dd>
																	<ul class="clearfix">
																		<li v-if="sortSelectData.listData[12].setting.show">
																			<span>링크클릭</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[12].setting.show">
																			<span>CTR</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[12].setting.show">
																			<span>CPC</span>
																			<span class="sort_btn"></span>
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
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>2번</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>3번</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>4번</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>5번</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[13].setting.show">
																			<span>6번</span>
																			<span class="sort_btn"></span>
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
																			<span>3초 이상 View</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>3초 이상 VTR</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>3초 이상 CPV</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>10초 이상 View</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>10초 이상 VTR</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[14].setting.show">
																			<span>10초 이상 CPV</span>
																			<span class="sort_btn"></span>
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
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>전환 완료 가치</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>1단계 완료</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>2단계 완료</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>3단계 완료</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>4단계 완료</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[15].setting.show">
																			<span>5단계 완료</span>
																			<span class="sort_btn"></span>
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
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>좋아요</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>댓글</span>
																			<span class="sort_btn"></span>
																		</li>
																		<li v-if="sortSelectData.listData[16].setting.show">
																			<span>공감</span>
																			<span class="sort_btn"></span>
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
															<li class="line-1" v-if="sortSelectData.listData[0].setting.show">광고주</li>
															<li class="line-2 normal_depth" v-if="sortSelectData.listData[1].setting.show">{{ item.campaign_name }}</li>
															<li class="line-3" v-if="sortSelectData.listData[2].setting.show">{{ item.report_date }}</li>
															<li class="line-4 normal_depth" v-if="sortSelectData.listData[3].setting.show">{{ item.adset_name }}</li>
															<li class="line-5" v-if="sortSelectData.listData[4].setting.show">{{ item.age }} 세</li>
															<li class="line-6" v-if="sortSelectData.listData[5].setting.show">{{ item.gender }}</li>
															<li class="interest line-7" v-if="sortSelectData.listData[6].setting.show">
																<span :class="'interest-sub-' + index" @click="tootip(index)">{{ item.interest_num }} 번</span>
																<div :id="'interest-sub-' + index" class="interest_view">
																	<ul class="clearfix">
																		<li>겉옷</li>
																		<li>데님</li>
																		<li>미니스커트</li>
																		<li>민소매셔츠</li>
																		<li>바지</li>
																		<li>반바지</li>
																		<li>블라우스</li>
																		<li>셔츠</li>
																		<li>쇼핑 및 패션</li>
																		<li>슈트</li>
																	</ul>
																	<div class="inter_clip_copy">클립보드로 복사하기</div>
																	<div class="inter_close" @click="tootip('close')">닫기</div>
																</div>
															</li>
															<li class="line-8 normal_depth" v-if="sortSelectData.listData[7].setting.show">맛춤타겟</li>
															<li class="line-9" v-if="sortSelectData.listData[8].setting.show">광고비</li>
															<li class="line-10" v-if="sortSelectData.listData[9].setting.show">{{ item.impressions }}</li>
															<li class="line-11" v-if="sortSelectData.listData[10].setting.show">도달</li>
															<li class="line-12" v-if="sortSelectData.listData[11].setting.show">3초 이상 CPV</li>
															<li class="line-13 depth1" v-if="sortSelectData.listData[12].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li>{{ item.link_click }}</li>
																			<li>{{ item.ctr }}</li>
																			<li>{{ item.cpc }}</li>
																		</ul>
																	</dd>
																</dl>
															</li>
															<li class="line-14 depth2" v-if="sortSelectData.listData[13].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li>1단계 완료</li>
																			<li>1단계 완료</li>
																			<li>1단계 완료</li>
																			<li>1단계 완료</li>
																			<li>1단계 완료</li>
																			<li>1단계 완료</li>
																		</ul>
																	</dd>
																</dl>
															</li>
															<li class="line-15 depth3" v-if="sortSelectData.listData[14].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li class="line-15" v-if="sortSelectData.listData[14].setting.show">좋아요</li>
																			<li class="line-15" v-if="sortSelectData.listData[14].setting.show">댓글</li>
																			<li class="line-15" v-if="sortSelectData.listData[14].setting.show">좋아요</li>
																			<li class="line-15" v-if="sortSelectData.listData[14].setting.show">댓글</li>
																			<li class="line-15" v-if="sortSelectData.listData[14].setting.show">공감</li>
																			<li class="line-15" v-if="sortSelectData.listData[14].setting.show">10초 이상 CPV</li>
																		</ul>
																	</dd>
																</dl>
															</li>

															<li class="line-16 depth4" v-if="sortSelectData.listData[15].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">좋아요</li>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">댓글</li>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">좋아요</li>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">댓글</li>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">공감</li>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">10초 이상 CPV</li>
																			<li class="line-16" v-if="sortSelectData.listData[15].setting.show">10초 이상 CPV</li>
																		</ul>
																	</dd>
																</dl>
															</li>
															<li class="line-17 depth5" v-if="sortSelectData.listData[16].setting.show">
																<dl>
																	<dt></dt>
																	<dd>
																		<ul>
																			<li class="line-17" v-if="sortSelectData.listData[16].setting.show">좋아요</li>
																			<li class="line-17" v-if="sortSelectData.listData[16].setting.show">댓글</li>
																			<li class="line-17" v-if="sortSelectData.listData[16].setting.show">좋아요</li>
																			<li class="line-17" v-if="sortSelectData.listData[16].setting.show">댓글</li>
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
									<div class="pagination">
										<ul>
											<li><img src="../../assets/images/icon/paging_01.png" alt=""></li>
											<li><img src="../../assets/images/icon/paging_03.png" alt=""></li>
											<li class="now">1</li>
											<li>2</li>
											<li><img src="../../assets/images/icon/paging_04.png" alt=""></li>
											<li><img src="../../assets/images/icon/paging_02.png" alt=""></li>
										</ul>
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
import Calendar from '@/components/ui/Calendar'

export default {
	name: 'TargetReport',

	components: {
		'ui-select': Select,
		'ui-calendar':Calendar
	},
	beforeMount() {
		this.setDatas()
	},
	mounted() {
		this.sortTableAutoWidth()
		this.wResize()
		window.addEventListener('resize', this.wResize)
	},
	beforeDestroy() {
		window.removeEventListener('resize', this.wResize)
	},
	data () {
		return {
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
				]
			},
			accountSelectData: {
				emptyText: '전체',
				textList: [
					'전체',
					'광고계정1',
					'광고계정2',
					'광고계정3'
				]
			},
			sortSelectData: {
				emptyText: '열 맞춤 설정',
				onShow:false,
				listData: [],
			},

			listData:{
				data: [
					{
						ctr: 1.4480365,
						'offsite_conversion.fb_pixel_purchase': {
							name: "Purchase",
							value: 28
						},
						video_view: 6323,
						post_engagement: 7337,
						adset_id: "6094357712857",
						'offsite_conversion.fb_pixel_add_to_cart': {
							name: "AddToCart",
							value: 113
						},
						impressions: 78272,
						clicks: 1135,
						age: "21-54",
						gender: "all",
						offsite_conversion: 286,
						cpc: 387.2416865,
						report_date: "2018-01-13 ~ 2018-01-14",
						reach: 43202,
						conversions: 7481,
						post_reaction: 12,
						'offsite_conversion.fb_pixel_add_payment_info': {
							name: "AddPaymentInfo",
							value: 2
						},
						objective: "CONVERSIONS",
						page_engagement: 7338,
						landing_page_view: 485,
						link_click: 995,
						spend: 437104,
						interest_num: 0,
						'offsite_conversion.custom.164727177414087': {
							name: "온리유 발급",
							value: 2
						},
						'offsite_conversion.custom.601949109998868': {
							name: "톡톡카드_자세히보기",
							value: 28
						},
						like: 1,
						adset_name: "톡톡_방문자_30일",
						cpp: 10118.428927,
						video_30_sec_watched_actions: 990,
						video_10_sec_watched_actions: 1237,
						campaign_name: "전환_톡톡_F",
						inline_link_clicks: 995,
						'offsite_conversion.custom.741750505927957': {
							name: "톡톡카드_발급",
							value: 113
						},
						post: 7
					},
					{
						ctr: 1.4480365,
						'offsite_conversion.fb_pixel_purchase': {
							name: "Purchase",
							value: 28
						},
						video_view: 6323,
						post_engagement: 7337,
						adset_id: "6094357712857",
						'offsite_conversion.fb_pixel_add_to_cart': {
							name: "AddToCart",
							value: 113
						},
						impressions: 78272,
						clicks: 1135,
						age: "21-54",
						gender: "all",
						offsite_conversion: 286,
						cpc: 387.2416865,
						report_date: "2018-01-13 ~ 2018-01-14",
						reach: 43202,
						conversions: 7481,
						post_reaction: 12,
						'offsite_conversion.fb_pixel_add_payment_info': {
							name: "AddPaymentInfo",
							value: 2
						},
						objective: "CONVERSIONS",
						page_engagement: 7338,
						landing_page_view: 485,
						link_click: 995,
						spend: 437104,
						interest_num: 0,
						'offsite_conversion.custom.164727177414087': {
							name: "온리유 발급",
							value: 2
						},
						'offsite_conversion.custom.601949109998868': {
							name: "톡톡카드_자세히보기",
							value: 28
						},
						like: 1,
						adset_name: "톡톡_방문자_30일",
						cpp: 10118.428927,
						video_30_sec_watched_actions: 990,
						video_10_sec_watched_actions: 1237,
						campaign_name: "전환_톡톡_F",
						inline_link_clicks: 995,
						'offsite_conversion.custom.741750505927957': {
							name: "톡톡카드_발급",
							value: 113
						},
						post: 7
					}
				],
				total_count: 1,
				success: "YES"
			},

			tablesAutoWidth:4880,



			show: false,
			time: new Date(),
			range: [new Date(),new Date()],
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
			}
		}
	},
	methods: {
		wResize(){
			const wSize = window.innerWidth - 185
			const el = document.getElementById('report-widget')
			el.style = "width:" + wSize + 'px'
		},
		tootip(index) {
			const tools = document.getElementsByClassName('interest_view')
			const subId = event.target.className
			const subEl = document.getElementById(subId)
			for(let i = 0; i < tools.length; i++) {
				tools[i].style = "display:none"
			}
			if(index != 'close') {
				if(subEl.style.display == 'block') {
					subEl.style = "display:none"
				}else{
					subEl.style = "display:block"
				}
			}
		},
		setDatas() {

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
		selectCategory(item) {
			this.categorySelectData.emptyText = item
		},
		selectAccount(item) {
			this.accountSelectData.emptyText = item
		},
		sortSelectOnOff() {
			this.sortSelectData.onShow = !this.sortSelectData.onShow
		},
		sortSelectFilter(item) {
			const me = this
			item.setting.checked = !item.setting.checked
			item.setting.show = !item.setting.show
			setTimeout(function() {
				me.sortTableAutoWidth()
			}, 1)
		},
		sortTableAutoWidth(){
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
		disabledDate (time) {
			return time < this.min || time > this.max
		},
		dc (e) {
			this.show = this.$el.contains(e.target) && !this.disabled
		}
	}
}
</script>

<style lang="css" scoped>
</style>
