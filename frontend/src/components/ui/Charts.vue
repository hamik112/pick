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
	        data:['테스트1','테스트2'],
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
	      data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
	      axisPointer: {
	            type: 'shadow'
	        }
	    },
	    yAxis: {},
	    series: [
		    {
	            name:'테스트1',
	            type:'bar',
	            data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
	        },
	        {
	            name:'테스트2',
	            type:'bar',
	            data:[2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
	        }
	    ]
	  }
	}),
	methods: {
	  doRandom() {
	    const that = this;
	    let data = [];
	    for (let i = 0, min = 5, max = 99; i < 6; i++) {
	      data.push(Math.floor(Math.random() * (max + 1 - min) + min));
	    }
	    that.bar.series[0].data = data;
	  },
	  onReady(instance) {
	    console.log(instance);
	  },
	  onClick(event, instance, echarts) {
	    console.log(arguments);
	  }
	}
}

</script>