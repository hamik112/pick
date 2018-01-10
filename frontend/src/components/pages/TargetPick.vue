<template>
	<div id="main_wrap" class="clearfix">

		<transition name='modal'>
			<TargetChartPop v-if="chartModal" @close="chartModal = false"></TargetChartPop>
			<TargetMake1 v-if="makeModal1" @close="makeModal1 = false"></TargetMake1>
			<TargetMake2 v-if="makeModal2" @close="makeModal2 = false"></TargetMake2>
		</transition>

		<div id="container">
			<div id="container_wrap">
				<div class="list-tab-widget">
					<div class="tab-contents-widget">
						<div id="section_list_1" class="section_tab_contents clearfix">
							<div class="target_aside">
								<ul>
									<li class="on">전체<span>21</span></li>
									<li>사이트방문<span>21</span></li>
									<li>특정페이지 방문<span>21</span></li>
									<li>NEO 타겟<span>21</span></li>
									<li>UTM 티켓<span>21</span></li>
									<li>구매<span>21</span></li>
									<li>장바구니<span>21</span></li>
									<li>회원가입<span>21</span></li>
									<li>단계별전환<span>21</span></li>
								</ul>
							</div>
							<div class="target_contents_wrap">
								<div class="target_setup">
									<ui-select :selectData="this.selectData" :onClick="selectTarget"></ui-select>
									<button type="button" @click="makeModal2 = true">타겟만들기</button>
								</div>
								<div class="target_contents">
									<ul>
										<li @click="chartModal = true">
											<div class="target_icon">
												<div class="icon_target on"></div>
												<div class="icon_gragh"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target"></div>
												<div class="icon_gragh on"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target on"></div>
												<div class="icon_gragh on"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target"></div>
												<div class="icon_gragh"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target"></div>
												<div class="icon_gragh"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target"></div>
												<div class="icon_gragh"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target"></div>
												<div class="icon_gragh"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li>
											<div class="target_icon">
												<div class="icon_target"></div>
												<div class="icon_gragh"></div>
											</div>
											<div class="target_info">
												<p>방문 고객_30일간</p>
												<p>규모가 작음</p>
											</div>
											<div class="target_state">
												<p>특정 페이지 방문</p>
												<p>000일</p>
												<p>특정 구매금액 이상 구매</p>
												<p>00,000원</p>
											</div>
										</li>
										<li class="target_last"><a href="javascript:void(0);" @click="makeModal1 = true"><img src="../../assets/images/common/target_add.jpg" alt=""></a></li>
									</ul>
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
	// 팝업
	import TargetChartPop from '@/components/popup/Target_chart'
	import TargetMake1 from '@/components/popup/Target_make_01'
	import TargetMake2 from '@/components/popup/Target_make_02'
	// UI
	import Select from '@/components/ui/Select'
	import Calendar from '@/components/ui/Calendar'

	export default {
		name: 'TargetPick',

		components: {
			'TargetChartPop': TargetChartPop,
			'TargetMake1': TargetMake1,
			'TargetMake2': TargetMake2,
			'ui-select': Select,
			'ui-calendar':Calendar
		},

		data () {
			return {
				chartModal: false,
				makeModal1: false,
				makeModal2: false,
				selectData: {
					emptyText: '전체보기',
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

<style lang="css" scoped>
</style>
