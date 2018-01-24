<template>
	<div class="modal-mask">
		<div class="modal-wrapper">
			<div class="modal-container">
				<div class="layer-pop-widget">
					<div class="popup-widget" id="target_chart">
						<div class="popup-contents clearfix">
							<div class="pop_title_wrap">
								<div class="pop_title">타겟 Chart</div>
								<p class="popup-btn"><button type="button" id="close-btn" class="close-btn close_pop" @click="$emit('close')"><img src="../../assets/images/target/white_close_i.png" alt=""></button></p>
							</div>
							<div class="target_chart_graph_wrap pop-scroll">
								<div class="target_chart_graph_inner clearfix ">
									<div class="target_chart_select clearfix">
										<div class="select_btn">
											<div class="select_contents">
												<!-- <div class="select"><p>오늘:2017/11/13</p></div> -->
												<ui-calendar v-model="range"></ui-calendar>
											</div>
										</div>
									</div>
									<div class="target_chart_top clearfix">
										<div class="use_limit clearfix">
											<div>
												<span>장바구니 이용고객_7일간</span>
												<ui-hover></ui-hover>
											</div>
											<p>글자수제한</p>
											<strong>6,500명</strong>
										</div>
										<div class="expense_price">
											<p>총 지출 금액(원)</p>
											<p>1,152,352,000</p>
										</div>
										<div class="all_switch">
											<p>총 전환</p>
											<p>3,512</p>
										</div>
										<div class="cpa_chart">
											<p>CPA</p>
											<p>815</p>
										</div>
									</div>
									<div class="target_chart_wrap">
										<div>
											<h2>인구 통계학적 특성</h2>
											<div class="graph_type01">
												<ui-charts :chartData="this.chart1"></ui-charts>
											</div>
										</div>
										<div>
											<h2>노출위치</h2>
											<div class="graph_type02">
												<ui-charts :chartData="this.chart2"></ui-charts>
											</div>
										</div>
									</div>
								</div>
								<div class="chart_close_btn close_pop" @click="$emit('close')">닫기</div>
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
import Charts from '@/components/ui/Charts'
import Calendar from '@/components/ui/Calendar'
import Hover from '@/components/ui/Hover'

export default {
	name: 'TargetChartPop',
	
  components: {
		'ui-select': Select,
		'ui-charts': Charts,
		'ui-calendar': Calendar,
		'ui-hover': Hover
	},
	
  data () {
		return {
			//charts Data sample
			chart1: {
				legend: ['모든남성 50%(3,250)','모든 여성 50%(3,250)'],
				xAxis: ['13-17세','18-24세','25-34세','35-44세','45-54세','55-64세','65세이상'],
				yAxis: {
					'type':'value',
					'name':'%',
					'max':100
				},
				
				series:[
					{
						name:'모든남성 50%(3,250)',
						type:'bar',
						data:[22, 63, 78, 33, 27, 25, 31],
						barWidth: '10%',

						itemStyle:{
							normal: {
								label : {
									show: true,
									position: 'insideRight',
									formatter: '{c}%'
								},
								color: '#58cefc'
							}
						}
					},
					{
						name:'모든 여성 50%(3,250)',
						type:'bar',
						data:[33, 22, 44, 66, 23, 87, 21],
						barWidth: '10%',
						itemStyle:{
							normal: {
								label : {
									show: true,
									position: 'insideLeft',
									formatter: '{c}%'
								},
								color: '#ff81c0'
							}
						}
					}
				]
			},
			chart2:{
				//네임
				legend: ['PC','Mobile'],

				//X데이터 네임
				xAxis: ['FaceBook','Audience Network','Instagram','Messanger'],

				yAxis: {
					'type':'value',
					'name':'K',
					'max':6
				},

				//순차적 데이터
				series:[
					{
						name: 'PC',
						type: 'bar',
						data: [4.3, 2.5, 5.0, 2.2, 1.6],
						barWidth: '5%',
						itemStyle: {
							normal: {
								label : {
									show: true,
									position: 'insideRight',
									formatter: '{c}K'
								},
								color: '#267aa9'
							}
						}
					},
					{
						name: 'Mobile',
						type: 'bar',
						data: [2.6, 5.9, 4.0, 5.4, 3.7],
						barWidth: '5%',
						itemStyle: {
							normal: {
								label: {
									show: true,
									position: 'insideLeft',
									formatter: '{c}K'
								},
								color:'#45ceb4'
							}
						}
					}
				]
			},

			//calendar
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
  }
}
</script>

<style lang="css" scoped>
</style>
