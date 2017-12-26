<template>
	<div id="main_wrap" class="clearfix">
		<Header></Header>
		<div id="container">
			<Aside></Aside>
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div class="tab-contents-widget">
						<div id="section_list_2" class="section_tab_contents clearfix">
							<div class="target_contents_wrap">
								<div class="target_search_wrap clearfix">
									<div class="cate_select">
										<p>카테고리</p>
										<div class="select_btn">
											<div class="select_contents">
												<div class="select"><p>전체</p></div>
												<ul class="select_view">
													<li>이벤트1</li>
													<li>이벤트2</li>
													<li>이벤트3</li>
												</ul>
											</div>
										</div>
									</div>
									<div class="admin_select">
										<p>광고계정</p>
										<div class="select_btn">
											<div class="select_contents">
												<div class="select"><p>전체</p></div>
												<ul class="select_view">
													<li>이벤트1</li>
													<li>이벤트2</li>
													<li>이벤트3</li>
												</ul>
											</div>
										</div>
									</div>
									<div class="data_select">
										<p>기간</p>
										<div class="select_btn">
											<div class="select_contents">
												<div class="select"><p class="calendar">오늘: 2017/11/13</p></div>
											</div>
										</div>
									</div>
									<button>검색</button>
								</div>
								<div class="target_report_wrap">
									<div class="target_setup">
										<div class="select_btn">
											<div class="select_contents test01">
												<div class="select"><p>열 맞춤 설정</p></div>
												<ul class="select_view test01_view">
													<li><input type="checkbox" id="sort01"><label for="sort01"></label>이벤트1</li>
													<li><input type="checkbox" id="sort02"><label for="sort02"></label>이벤트2</li>
													<li><input type="checkbox" id="sort03"><label for="sort03"></label>이벤트3</li>
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
											<table>
												<thead>
													<tr>
														<th rowspan="2">광고주</th>
														<th rowspan="2">캠페인명</th>
														<th rowspan="2">기간</th>
														<th rowspan="2">광고세트</th>
														<th rowspan="2">연령</th>
														<th rowspan="2">성별</th>
														<th rowspan="2">관심사 개수</th>
														<th rowspan="2">맞춤타겟 이름</th>
														<th rowspan="2">광고비</th>
														<th rowspan="2">노출</th>
														<th rowspan="2">도달</th>
														<th rowspan="2">도달빈도</th>
														<th rowspan="2" colspan="3">사이트 유입 지표</th>
														<th rowspan="2" colspan="6">슬라이드 소재 클릭 지표</th>
														<th rowspan="2" colspan="6">영상캠페인 지표</th>
														<th rowspan="2" colspan="7">전환 지표</th>
														<th rowspan="2" colspan="4">페이지 참여 지표</th>
													</tr>
													<tr>
														<td>123</td>
														<td>123</td>
														<td>123</td>
														<td>123</td>
														<td>123</td>
														<td>123</td>
														<td>123</td>
														<td>123</td>
														<td>123</td>
													</tr>
												</thead>
												<tbody>
												</tbody>
											</table>
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
		<Footer></Footer>
	</div>
</template>

<script>
	//레이아웃 호출
	import Header from '@/components/layout/Header'
	import Footer from '@/components/layout/Footer'
	import Aside from '@/components/layout/Aside'
	export default {

	  name: 'TargetReport',
	  components: {'Header': Header,'Footer': Footer,'Aside': Aside},

	  data () {
	    return {

	    }
	  }
	}
</script>

<style lang="css" scoped>
</style>