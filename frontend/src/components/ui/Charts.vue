<template>
	<div class="echarts">
		<IEcharts :option="bar" :resizable="true" @ready="onReady" @click="onClick"></IEcharts>
	</div>
</template>

<script>
import IEcharts from 'vue-echarts-v3'
// import ECharts.js modules manually to reduce bundle size
import 'echarts/lib/chart/bar'

export default {
	name: 'Charts',

	components: {
	  IEcharts
	},

	props: {
		chartData: {
			type: Object,
			default () {
				return {
					tooltip:{},
					legend:[],
					xAxis: [],
					yAxis:{},
					series:[]
				}
			}
		}
	},
	data: () => ({
	  loading: true,
	  bar: {
	    title: {
	      text: ''
	    },
	    tooltip: {
	    	trigger: 'axis',
	        axisPointer: {
	            type: 'cross',
	            crossStyle: {
	                color: '#999'
	            }
	        }
	    },
	    toolbox:{
	    	show: false,
            right: '7%',
            top: '0',
            feature: {
                mark: {
                    show: false,
                    title: {
                        mark: 'mark',
                        markUndo: 'markUndo',
                        markClear: 'markClear'
                    },
                    lineStyle: {
                        width: 2,
                        color: '#1e90ff',
                        type: 'dashed'
                    }
                },
                dataZoom: {
                    yAxisIndex: 'none',
                    show: true,
                    title : {
                        zoom : '영역확대',
                        back : '뒤로가기'
                    }
                },
                magicType: {
                    show: true,
                    title: {
                        line: '라인',
                        bar: '그래프',
                        stack: 'stack',
                        tiled: 'tiled',
                        force: 'force',
                        chord: 'chord',
                        pie: '파이',
                        funnel: 'funnel'
                    }
                },
                restore: {
                    show: true,
                    title: '업데이트'
                },
                saveAsImage: {
                    show: false,
                    title: '이미지저장'
                }
            }
	    },
	    legend: {
	        data:[],
	        bottom: 10
	    },
	    grid: {
            left: 50,
            right: '8%',
            top:50,
            bottom: '13%',
            containLabel: true
        },
	    xAxis: {
	      data: [],
	      axisPointer: {
	          type: 'shadow'
	      }
	    },
	    yAxis: {},
	    series: [],
	    colors:['#5793f3', '#d14a61', '#675bba']
	  }
	}),
	methods: {
	  doRandom() {
	    // const that = this
	    // let data = []
	    // for (let i = 0, min = 5, max = 99; i < 6; i++) {
	    //   data.push(Math.floor(Math.random() * (max + 1 - min) + min))
	    // }
	    // that.bar.series[0].data = data;
	  },
	  onReady(instance) {
	  	const bar = this.bar

	  	bar.legend.data = this.chartData.legend
	    bar.xAxis.data = this.chartData.xAxis
	    bar.yAxis = this.chartData.yAxis
	    bar.series = this.chartData.series
	  },
	  onClick(event, instance, echarts) {
	    console.log(arguments);
	  }
	}
}

</script>