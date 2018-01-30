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
												<ui-PartialLoading  v-if="!chartOn" />
												<ui-charts :chartData="this.chartGenderData" v-if="chartOn"></ui-charts>
											</div>
										</div>
										<div>
											<h2>노출위치</h2>
											<div class="graph_type02">
												<ui-PartialLoading v-if="!chartOn" />
												<ui-charts :chartData="this.chartPlacementData" v-if="chartOn"></ui-charts>
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
import PartialLoading from '@/components/ui/partialLoading'
import { numberToFixed } from '@/components/utils/formatter'

export default {
  name: 'TargetChartPop',

  components: {
		'ui-select': Select,
		'ui-charts': Charts,
		'ui-calendar': Calendar,
		'ui-hover': Hover,
		'ui-PartialLoading': PartialLoading
  },

  props:{
  	chartItem: {
  		type:Object,
  		default () {
  			return {}
  		}
  	}
  },
  created() {
  	const targetId = this.chartItem.id
  	this.$http.get('/pickdata_account_target/target_chart', {
  		params: {
			pickdata_target_id:targetId,
		}
    })
    .then(res => {
      const response = res
      const success = response.status
      if (success === 200) {
      	let data = response.data
      	//genderData
      	this.chartGenderData.series[0]['data'] = this.chartsRedatas(data.age_gender_data.data.male.percents, 2)
      	this.chartGenderData.series[1]['data'] = this.chartsRedatas(data.age_gender_data.data.female.percents, 2)
      	//placementsData
      	this.chartPlacementData['legend'] = data.placement_data.legend
      	this.chartPlacementData['xAxis'] = data.placement_data.xAxis
      	this.chartPlacementData.series[0]['data'] = data.placement_data.data.PC.vals
      	this.chartPlacementData.series[1]['data'] = data.placement_data.data.Mobile.vals

      	this.chartOn = true
      }else{
      	throw('success: ' + success)
      }

    })
  },

  data () {
		return {
			//loading
			chartOn:false,


			//chartGenderData
			chartGenderData: {
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
						data:[],
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
						data:[],
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

			//chartPlacementData
			chartPlacementData:{
				//네임
				legend: [],

				//X데이터 네임
				xAxis: [],

				yAxis: {
					'type':'value',
					'name':'K'
				},

				//순차적 데이터
				series:[
					{
						name: 'PC',
						type: 'bar',
						data: [],
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
						data: [],
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
  },
  methods: {
  	chartsRedatas(data) {
  		const reDatas = []
  		for(let i = 0; i < data.length; i++) {
  			reDatas.push(numberToFixed(data[i]))
  		}
  		return reDatas
  	}
  }
}
</script>

<style lang="css" scoped>
.graph_type01,
.graph_type02 { overflow:hidden; }
</style>
